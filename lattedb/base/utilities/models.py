"""Help functions to inspect models
"""
from typing import Optional
from typing import Tuple
from typing import List

from django.db import models
from django.apps import apps
from django.apps.config import AppConfig

from lattedb.config.settings import PROJECT_APPS

from lattedb.base.utilities.blackmagicsorcery import concludo_expressum
from lattedb.base.models import Base


def get_project_apps(exclude_apps: Optional[Tuple[str]] = None) -> List[AppConfig]:
    """Finds all apps which are part of the project.

    Iterates over apps specified in the settings.yaml file and returns django app configs
    if installed.
    """
    exclude_apps = list(exclude_apps) if exclude_apps is not None else []
    exclude_apps += ["lattedb.base", "lattedb.documentation"]

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


def get_lattedb_models(exclude_apps: Optional[Tuple[str]] = None) -> models.Model:
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
