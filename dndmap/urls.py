from django.contrib import admin
from django.urls import path, include

from .views import main as views_main
from .views import map as views_map
from .views import components as views_components

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", views_main.index, name="index"),
    path("map/", views_map.ListView.as_view(), name="list_map"),
    path("map/add/", views_map.CreateView.as_view(), name="create_map"),
    path("map/<int:pk>/", views_map.get_map, name="show_map"),
    path("map/<int:pk>/components", views_components.get_components, name='get_components'),
    path("map/<int:pk>/components/add", views_components.add_new_marker, name='add_new_marker'),
]
