from django.contrib import admin

from dndmap.models import Map, Layer, Marker


@admin.register(Map)
class MapAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner")


@admin.register(Layer)
class LayerAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "map")


@admin.register(Marker)
class MarkerAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "layer")
