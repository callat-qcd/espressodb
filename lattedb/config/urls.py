# pylint: disable=C0103
"""lattedb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os

from django.contrib import admin
from django.urls import path, include

from lattedb.config.settings import PROJECT_APPS, ROOT_DIR
from lattedb.config.views import IndexView

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
    path("", IndexView.as_view(), name="index"),
]
