from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import ValidationError
from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic

from dndmap.models import Party, User


def party_view(request):
    context = {}
    if request.user.party:
        context['members'] = User.objects.filter(party=request.user.party).values_list('username', flat=True)
    return render(request, 'party.html', context)


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


class UpdateView(PermissionRequiredMixin, LoginRequiredMixin, generic.UpdateView):
    model = Party
    template_name = "party/update.html"
    fields = ["name"]

    def has_permission(self):
        return Party.objects.get(id=self.kwargs['pk']).admin == self.request.user

    def get(self, request, *args, **kwargs):
        self.extra_context = {
            'members': User.objects.filter(party_id=self.kwargs['pk']).values('id', 'username')
        }
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(
            self.request,
            f'Renamed your party to "{self.object.name}"',
            'alert-success',
        )
        return reverse("party")


def delete_party_member(request, party_id, user_id):
    if Party.objects.get(id=party_id).admin != request.user:
        raise ValidationError('You are not the admin for this party.')
    if user_id == request.user.id:
        raise ValidationError('Cannot delete the admin of this party.')
    user_to_delete = User.objects.get(id=user_id)
    user_to_delete.delete()
    messages.success(request, f'Deleted user {user_to_delete.username}.', 'alert-success')
    return redirect(reverse('party'))
