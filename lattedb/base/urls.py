# pylint: disable=C0103
"""Url patters for base
"""
from django.urls import path

from lattedb.base import views

app_name = "Base"
urlpatterns = [
    path("populate", views.PopulationView.as_view(), name="populate"),
    path(
        "populate-result", views.PopulationResultView.as_view(), name="populate-result"
    ),
    path("", views.index, name="index"),
]
