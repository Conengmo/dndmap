import json

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse, HttpResponse

from dndmap.decorators import get_map_obj
from dndmap.models import Map, Marker, Layer


@get_map_obj
@login_required
def get_components(request: HttpRequest, map_obj: Map):
    return JsonResponse(
        [layer.to_dict() for layer in map_obj.layer_set.all()],
        safe=False,
    )


@get_map_obj
@login_required
def upsert_marker(request: HttpRequest, map_obj: Map):
    data = json.loads(request.body)
    layer_id = data.pop('layer_id')
    layer = Layer.objects.get(pk=layer_id)
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
