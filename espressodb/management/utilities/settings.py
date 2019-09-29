"""Provides package settings variables needed by espressodb
"""
from django.conf import settings

from django.core.exceptions import ImproperlyConfigured


PROJECT_APPS = getattr(settings, "PROJECT_APPS", None)

if PROJECT_APPS is None:
    raise ImproperlyConfigured(
        "Could not import `PROJECT_APPS`."
        " Please set this list of apps in your root settings module."
    )


ROOT_DIR = getattr(settings, "ROOT_DIR", None)

if ROOT_DIR is None:
    raise ImproperlyConfigured(
        "Could not import `ROOT_DIR`."
        " Please set this directory in your root settings module."
    )

PROJECT_NAME = getattr(settings, "PROJECT_NAME", None)

if PROJECT_NAME is None:
    raise ImproperlyConfigured(
        "Could not import `PROJECT_NAME`."
        " Please set this variable in your root settings module."
    )
