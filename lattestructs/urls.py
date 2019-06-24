# pylint: disable=C0103
"""Url patters for lattestructs
"""
from django.urls import path

from lattestructs import views

urlpatterns = [path("", views.index, name="index")]
