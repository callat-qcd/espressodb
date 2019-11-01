"""Functions to identify project apps
"""
from typing import Optional
from typing import Tuple
from typing import List
from typing import Dict

from django.apps.config import AppConfig
from django.apps import apps as django_apps

from django.template.defaultfilters import slugify

from espressodb.management.utilities.settings import PROJECT_APPS
from espressodb.base.utilities.blackmagicsorcery import search


def get_project_apps(exclude_apps: Optional[Tuple[str]] = None) -> List[AppConfig]:
    """Finds all apps which are part of the project.

    Arguments:
        exclude_apps:
            Name of the apps to exclude. Must match ``settings.yaml`` specification.

    Iterates over apps specified in the settings.yaml file and returns django app configs
    if installed.
    """
    exclude_apps = list(exclude_apps) if exclude_apps is not None else []
    exclude_apps += ["espressodb.base", "espressodb.documentation"]

    installed_apps = {app.name: app for app in django_apps.app_configs.values()}

    available_apps = []

    for app_path in PROJECT_APPS:
        if (
            any([search(exclude, app_path) for exclude in exclude_apps])
            or not app_path in installed_apps
        ):
            continue

        available_apps.append(installed_apps[app_path])

    return available_apps


def get_app_name(app: AppConfig) -> str:
    """Returns a readable name for the app

    Arguments:
        app: The app config.
    """
    return " ".join([s.capitalize() for s in app.name.split(".")[1:]])


def get_apps_slug_map() -> Dict[str, str]:
    """Creates a map for all project app names. Keys are slugs, values are names.
    """
    slug_map = {}
    for app in get_project_apps():
        name = get_app_name(app)
        slug_map[slugify(name)] = app
    return slug_map


APPS_TO_SLUG = {app: slug for slug, app in get_apps_slug_map().items()}
