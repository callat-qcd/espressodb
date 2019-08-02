"""Help functions to inspect models
"""
from typing import Optional
from typing import Tuple

from django.db import models
from django.apps import apps

from lattedb.config.settings import PROJECT_APPS
from lattedb.base.utilities.blackmagicsorcery import metamorph
from lattedb.base.utilities.blackmagicsorcery import concludo_expressum


def get_lattedb_models(exclude_apps: Optional[Tuple[str]] = None) -> models.Model:
    """Returns all project models which are not in the exclude list
    """
    exclude_apps = list(exclude_apps) if exclude_apps is not None else []
    exclude_apps += ["lattedb.base", "lattedb.documentation"]

    app_models = []
    for app in PROJECT_APPS:
        if any([concludo_expressum(exclude, app) for exclude in exclude_apps]):
            continue
        app_name = metamorph("lattedb.", "", app)
        app_models += apps.get_app_config(app_name).get_models()

    return app_models
