# pylint: disable=C0103
"""Url patters for base
"""
from django.urls import path

from espressodb.base import views

urlpatterns = []

app_name = "base"
urlpatterns += [
    path("", views.IndexView.as_view(), name="index"),
    path("populate/", views.PopulationView.as_view(), name="populate"),
    path(
        "populate-result/", views.PopulationResultView.as_view(), name="populate-result"
    ),
]
