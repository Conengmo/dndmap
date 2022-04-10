from django.contrib import admin

from dndmap.models import Map, Layer, Marker


@admin.register(Map)
class MapAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "user")


@admin.register(Layer)
class MapAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "map")


@admin.register(Marker)
class MapAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "layer")
