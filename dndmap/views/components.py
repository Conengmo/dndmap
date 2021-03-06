import json

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods

from dndmap.decorators import get_map_obj
from dndmap.models import Map, Marker, Layer


@login_required
@get_map_obj
def get_components(request: HttpRequest, map_obj: Map):
    return JsonResponse(
        [layer.to_dict() for layer in map_obj.layer_set.all()],
        safe=False,
    )


@login_required
@get_map_obj
def upsert_marker(request: HttpRequest, map_obj: Map):
    data = request.POST.dict()
    layer_id = data.pop('layer_id')
    layer = Layer.objects.get(id=layer_id)
    if layer.map_id != map_obj.id:
        return HttpResponse(status=403)
    marker_id = data.pop('id') or None
    Marker.objects.update_or_create(
        id=marker_id,
        defaults=dict(
            layer=layer,
            **data,
        )
    )
    return HttpResponse()


@login_required
@get_map_obj
def update_marker_coords(request: HttpRequest, map_obj: Map):
    data = json.loads(request.body)
    Marker.objects.filter(id=data.pop('id'), layer__map=map_obj).update(**data)
    return HttpResponse()


@login_required
@get_map_obj
@require_http_methods(['POST'])
def upsert_layer(request: HttpRequest, map_obj: Map):
    data = request.POST.dict()
    layer_id = data.pop('id') or None
    Layer.objects.update_or_create(
        id=layer_id,
        map=map_obj,
        defaults=data,
    )
    return HttpResponse()
