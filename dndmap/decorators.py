from functools import wraps

from django.http import HttpResponse

from dndmap.models import Map


def get_map_obj(func):

    @wraps(func)
    def decorator(request, pk):
        map_obj = Map.objects.get(pk=pk)
        if map_obj.user != request.user:
            return HttpResponse(403)
        return func(request, map_obj)

    return decorator
