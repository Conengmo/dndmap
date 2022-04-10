from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from dndmap.decorators import get_map_obj
from dndmap.models import Map


class ListView(LoginRequiredMixin, generic.ListView):
    model = Map
    template_name = "map/list.html"

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class CreateView(LoginRequiredMixin, generic.CreateView):
    model = Map
    template_name = "map/create.html"
    fields = ["name", "file"]

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("show_map", kwargs={"pk": self.object.pk})


@get_map_obj
@login_required
def get_map(request: HttpRequest, map_obj: Map):
    context = {
        'map_obj': map_obj,
        'layers': {layer.pk: layer.name for layer in map_obj.layer_set.all()},
    }
    return render(request, 'map/map.html', context)
