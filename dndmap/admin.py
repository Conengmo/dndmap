from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from dndmap.models import Map, Layer, Marker, Party, User


class UserPartyInline(admin.TabularInline):
    model = User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {
            'fields': ('party',),
        }),
    )


@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    inlines = [UserPartyInline]


@admin.register(Map)
class MapAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "party")


@admin.register(Layer)
class LayerAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "map")


@admin.register(Marker)
class MarkerAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "layer")
