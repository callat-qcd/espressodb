"""Help functions to inspect models
"""
from typing import Optional
from typing import Tuple
from typing import List
from typing import Dict

from django.db import models
from django.apps import apps
from django.apps.config import AppConfig
from django.template.defaultfilters import slugify

from espressodb.config.settings import PROJECT_APPS
from espressodb.base.utilities.blackmagicsorcery import concludo_expressum
from espressodb.base.models import Base


def get_project_apps(exclude_apps: Optional[Tuple[str]] = None) -> List[AppConfig]:
    """Finds all apps which are part of the project.

    Iterates over apps specified in the settings.yaml file and returns django app configs
    if installed.
    """
    exclude_apps = list(exclude_apps) if exclude_apps is not None else []
    exclude_apps += ["espressodb.base", "espressodb.documentation"]

    installed_apps = {app.name: app for app in apps.app_configs.values()}

    available_apps = []

    for app_path in PROJECT_APPS:
        if (
            any([concludo_expressum(exclude, app_path) for exclude in exclude_apps])
            or not app_path in installed_apps
        ):
            continue

        available_apps.append(installed_apps[app_path])

    return available_apps


def get_app_name(app: AppConfig) -> str:
    """Returns a readable name for the app
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


def get_espressodb_models(exclude_apps: Optional[Tuple[str]] = None) -> models.Model:
    """Returns all installed project models which are not in the exclude list
    """
    return [
        model for app in get_project_apps(exclude_apps) for model in app.get_models()
    ]


def iter_tree(model: Base, name: Optional[str] = None) -> List[Tuple[str, str]]:
    """Extracts all foreign keys of model and inserters them in list.

    Returns strings in flat tree format, e.g., `propagator.gaugeconfig`.

    **Arguments**
        model: Base
            A child of the base model.

        name: Optional[str] = None
            The (path) name of the model.

    **Returns**
        tree: List[Tuple[str, str]]
            First element of tuple are name names of the foreign keys in format
            `{name}.{field.name}`.
            Second element are the actual classes.
    """
    tree = []

    for field in model.get_open_fields():
        if isinstance(field, models.ForeignKey):
            tree.append(
                (f"{name}.{field.name}" if name else field.name, field.related_model)
            )

    return tree
