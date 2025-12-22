from django.urls import path

from looseinventory.inventory.views import matches_view

app_name = "inventory"

urlpatterns = [
    path("matches/", matches_view, name="matches"),
]