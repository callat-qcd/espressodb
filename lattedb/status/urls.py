# pylint: disable=C0103
"""Url patters for base
"""
from django.urls import path

from lattedb.status import views

app_name = "Status"
urlpatterns = [path("baryon2pt", views.Baryon2ptProgressView.as_view(), name="progress")]
