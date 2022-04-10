import json

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse, HttpResponse

from dndmap.decorators import get_map_obj
from dndmap.models import Map, Marker


@get_map_obj
@login_required
def get_components(request: HttpRequest, map_obj: Map):
    return JsonResponse(
        [layer.to_dict() for layer in map_obj.layer_set.all()],
        safe=False,
    )


@get_map_obj
@login_required
def add_new_marker(request: HttpRequest, map_obj: Map):
    data = json.loads(request.body)
    Marker.objects.create(
        layer=map_obj.layer_set.first(),
        **data,
    )
    return HttpResponse()
