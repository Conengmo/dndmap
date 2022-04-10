from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import generic

from dndmap.models import Map


class ListView(LoginRequiredMixin, generic.ListView):
    model = Map
    template_name = 'map/list.html'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Map
    template_name = 'map/detail.html'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class CreateView(LoginRequiredMixin, generic.CreateView):
    model = Map
    template_name = 'map/create.html'
    fields = ['name', 'file']

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('map detail', kwargs={'pk': self.object.pk})
