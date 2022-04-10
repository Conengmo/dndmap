from django.contrib import admin

from dndmap.models import Map


@admin.register(Map)
class MapAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'user')
