from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from dndmap.models import Map, Layer, Marker, Party, User


class UserInline(admin.TabularInline):
    model = User
    fields = ['username']
    extra = 0


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'party', 'is_staff', 'date_joined')
    fieldsets = UserAdmin.fieldsets + (
        (None, {
            'fields': ('party',),
        }),
    )


@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    inlines = [UserInline]


@admin.register(Map)
class MapAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "party")


@admin.register(Layer)
class LayerAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "map")


@admin.register(Marker)
class MarkerAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "layer")
