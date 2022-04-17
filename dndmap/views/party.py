from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic

from dndmap.models import Party


def party_view(request):
    context = {
    }
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
        return self.request.user.party_id == self.kwargs['pk']

    def get_success_url(self):
        messages.success(
            self.request,
            f'Renamed your party to "{self.object.name}"',
            'alert-success',
        )
        return reverse("party")
