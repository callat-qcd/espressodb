# pylint: disable=C0103
"""Url patters for base
"""
import os

from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from espressodb.management.utilities.settings import PROJECT_APPS
from espressodb.management.utilities.settings import ROOT_DIR
from espressodb.base import views

urlpatterns = []

for app in PROJECT_APPS:
    url_file = os.path.join(ROOT_DIR, app.replace(".", "/"), "urls.py")
    if os.path.exists(url_file):
        _, app_name = app.split(".")
        if app_name == "config":
            continue
        urlpatterns.append(
            path(rf"{app_name}/", include(app + ".urls", namespace=app_name))
        )


urlpatterns += [
    path("admin/", admin.site.urls),
    path(
        "login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("populate", views.PopulationView.as_view(), name="populate"),
    path(
        "populate-result", views.PopulationResultView.as_view(), name="populate-result"
    ),
    path(
        r"documentation/",
        include("espressodb.documentation.urls", namespace="documentation"),
    ),
    path("", views.IndexView.as_view(), name="index"),
]
