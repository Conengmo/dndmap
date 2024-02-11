import os
import shutil

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpRequest
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
    fields = ["name", "file", "scale"]

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


def _map_to_static(map_obj: Map, destination: str):
    context = {
        'map_obj': map_obj,
        'components': [layer.to_dict() for layer in map_obj.layer_set.all()],
    }
    resp = render(HttpRequest(), 'map/static_map.html', context)
    html_bytes = resp.content
    html_bytes = html_bytes.replace(b"/static/tiles/", b"tiles/")
    shutil.copytree(
        map_obj.tiles_filepath,
        os.path.join(destination, "tiles", str(map_obj.id))
    )
    with open(os.path.join(destination, f"{map_obj.name.lower()}.html"), "wb") as f:
        f.write(html_bytes)


@login_required
def export_static_maps(request):
    map_objs = Map.objects.filter(party_id=request.user.party_id)
    context = {
        'maps': map_objs,
    }
    destination = "static_export"
    if os.path.exists(destination):
        shutil.rmtree(destination)
    shutil.copytree(
        settings.STATIC_ROOT / "awesome_markers",
        os.path.join(destination, "awesome_markers")
    )
    shutil.copy2(
        settings.STATIC_ROOT / "rastercoords.js",
        os.path.join(destination, "rastercoords.js")
    )
    resp = render(HttpRequest(), 'map/static_list.html', context)
    html_bytes = resp.content
    html_bytes = html_bytes.replace(b"/static/tiles/", b"tiles/")
    with open(os.path.join(destination, "index.html"), "wb") as f:
        f.write(html_bytes)
    for map_obj in map_objs:
        _map_to_static(map_obj, destination)
    messages.success(request, 'Exported maps as static files.', 'alert-success')
    return render(request, 'map/list.html', context)