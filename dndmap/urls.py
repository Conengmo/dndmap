from django.contrib import admin
from django.urls import path, include

from .views import main as views_main
from .views import map as views_map
from .views import components as views_components
from .views import party as views_party

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", views_main.index, name="index"),
    path("map/", views_map.list_maps, name="list_map"),
    path("map/add/", views_map.CreateView.as_view(), name="create_map"),
    path("map/export/", views_map.export_static_maps, name="export_static_maps"),
    path("map/<int:pk>/", views_map.get_map, name="show_map"),
    path("map/<int:pk>/static", views_map.export_static_maps, name="static_map"),
    path("map/<int:pk>/components", views_components.get_components, name='get_components'),
    path("map/<int:pk>/marker/add", views_components.upsert_marker, name='upsert_marker'),
    path("map/<int:pk>/marker/update-coordinates/", views_components.update_marker_coords, name="update_marker_coords"),
    path("map/<int:pk>/layer/add", views_components.upsert_layer, name='upsert_layer'),
    path("party/", views_party.party_view, name='party'),
    path("party/<int:pk>/", views_party.UpdateView.as_view(), name='update_party'),
    path("party/add/", views_party.CreateView.as_view(), name='create_party'),
    path("party/<int:pk>/member/add/", views_party.AddPartyMemberView.as_view(), name='add_party_member'),
    path("party/<int:pk>/member/<int:user_id>/delete/", views_party.DeletePartyMemberView.as_view(), name='delete_party_member'),
]
