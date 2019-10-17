"""Provides package settings variables needed by espressodb.

Raises ``ImproperlyConfigured`` errors if variables are not found.
"""
from typing import List

from django.conf import settings

from django.core.exceptions import ImproperlyConfigured


#: List of apps used in the project.
#: Will be added to Django's ``INSTALLED_APPS``
PROJECT_APPS: List[str] = getattr(settings, "PROJECT_APPS", None)

if PROJECT_APPS is None:
    raise ImproperlyConfigured(
        "Could not import `PROJECT_APPS`."
        " Please set this list of apps in your root settings module."
    )


#: Root directory of the current project
ROOT_DIR: str = getattr(settings, "ROOT_DIR", None)

if ROOT_DIR is None:
    raise ImproperlyConfigured(
        "Could not import `ROOT_DIR`."
        " Please set this directory in your root settings module."
    )

#: Name of the current project.
#: Must match the name of the project Python module
PROJECT_NAME: str = getattr(settings, "PROJECT_NAME", None)

if PROJECT_NAME is None:
    raise ImproperlyConfigured(
        "Could not import `PROJECT_NAME`."
        " Please set this variable in your root settings module."
    )
