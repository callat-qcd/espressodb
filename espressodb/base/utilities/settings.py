"""Provides package settings variables needed by espressodb
"""
from django.conf import settings

from django.core.exceptions import ImproperlyConfigured


PROJECT_APPS = settings.get("PROJECT_APPS", None)

if PROJECT_APPS is None:
    raise ImproperlyConfigured(
        "Could not import `PROJECT_APPS`."
        " Please set this list of apps in your root settings module."
    )


ROOT_DIR = settings.get("ROOT_DIR", None)

if ROOT_DIR is None:
    raise ImproperlyConfigured(
        "Could not import `ROOT_DIR`."
        " Please set this directory in your root settings module."
    )
