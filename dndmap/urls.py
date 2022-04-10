from django.contrib import admin
from django.urls import path, include

from .views import main as views_main
from .views import map as views_map

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", views_main.index, name="index"),
    path("map/", views_map.ListView.as_view(), name="map list"),
    path("map/<int:pk>/", views_map.DetailView.as_view(), name="map detail"),
    path("map/create/", views_map.CreateView.as_view(), name="map create"),
]
