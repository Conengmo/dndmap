from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic

from dndmap.models import Party, User


@login_required
def party_view(request):
    context = {}
    if request.user.party:
        context['members'] = User.objects.filter(party=request.user.party).values_list('username', flat=True)
    return render(request, 'party/party.html', context)


class CreateView(LoginRequiredMixin, generic.CreateView):
    model = Party
    template_name = "party/create.html"
    fields = ["name"]

    def get(self, request, *args, **kwargs):
        if request.user.party:
            messages.info(request, 'You are already in a party.', 'alert-info')
            return redirect(reverse('party'))
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        if self.request.user.party:
            raise ValidationError('This user is already in a party.')
        obj = form.save(commit=False)
        obj.admin = self.request.user
        response = super().form_valid(form)
        self.request.user.party = self.object
        self.request.user.save()
        return response

    def get_success_url(self):
        messages.success(
            self.request,
            f'Created party "{self.object.name}" and added you as a member',
            'alert-success',
        )
        return reverse("party")


class CheckUserIsPartyAdminMixin(PermissionRequiredMixin):

    def has_permission(self):
        return get_object_or_404(Party, id=self.kwargs['pk']).admin == self.request.user


class UpdateView(CheckUserIsPartyAdminMixin, LoginRequiredMixin, generic.UpdateView):
    model = Party
    template_name = "party/update.html"
    fields = ["name"]

    def get(self, request, *args, **kwargs):
        self.extra_context = {
            'members': User.objects.filter(party_id=self.kwargs['pk']).values('id', 'username'),
        }
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(
            self.request,
            f'Renamed your party to "{self.object.name}"',
            'alert-success',
        )
        return reverse("party")


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}


class AddPartyMemberView(CheckUserIsPartyAdminMixin, LoginRequiredMixin, generic.View):
    http_method_names = ['get', 'post']

    def get(self, request, pk):
        context = {'form': CustomUserCreationForm()}
        return render(request, 'party/add_member.html', context)

    def post(self, request, pk):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.party_id = pk
            new_user.save()
            messages.success(request, f'Created new user "{new_user.username}".', 'alert-success')
            return redirect('update_party', pk)
        else:
            context = {'form': form}
            return render(request, 'party/add_member.html', context)


class DeletePartyMemberView(CheckUserIsPartyAdminMixin, LoginRequiredMixin, generic.View):
    http_method_names = ['get']

    def get(self, request, pk, user_id):
        if user_id == request.user.id:
            messages.error(request, 'You cannot delete the admin of this party.', 'alert-danger')
            return redirect('update_party', pk)

        user_to_delete = get_object_or_404(User, id=user_id)
        user_to_delete.delete()
        messages.success(request, f'Deleted user {user_to_delete.username}.', 'alert-success')
        return redirect(reverse('party'))
