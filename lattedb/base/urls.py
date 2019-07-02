# pylint: disable=C0103
"""Url patters for base
"""
from django.urls import path

from lattedb.base import views

urlpatterns = [path("", views.index, name="index")]
