# pylint: disable=C0103
"""Url patters for base
"""
from django.urls import path

from lattedb.base import views

app_name = "Base"
urlpatterns = [
    path("populate", views.TableSelectView.as_view(), name="populate"),
    path("", views.index, name="index"),
]
