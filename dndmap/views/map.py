from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from dndmap.decorators import get_map_obj
from dndmap.models import Map, Marker


@login_required
def list_maps(request):
    context = {
        'maps': Map.objects.filter(party_id=request.user.party_id),
    }
    return render(request, 'map/list.html', context)


class CreateView(LoginRequiredMixin, generic.CreateView):
    model = Map
    template_name = "map/create.html"
    fields = ["name", "file"]

    def form_valid(self, form):
        obj = form.save(commit=False)
        if not self.request.user.party:
            raise ValidationError('You have to be in a party to create a map.')
        obj.party = self.request.user.party
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("show_map", kwargs={"pk": self.object.pk})


@login_required
@get_map_obj
def get_map(request, map_obj: Map):
    context = {
        'map_obj': map_obj,
        'maps': list(Map.objects.filter(party_id=request.user.party_id).values('id', 'name')),
        'layers': list(map_obj.layer_set.all()) + [{'name': '', 'id': '', 'show_at_zoom_level': map_obj.min_zoom}],
        'marker_color_options': Marker.ColorOptions.values,
    }
    return render(request, 'map/map.html', context)
