"""Help functions to inspect models
"""
from typing import Optional
from typing import Tuple
from typing import Dict
from typing import List
from typing import Any

from django.db import models
from django.apps import apps

from lattedb.config.settings import PROJECT_APPS

from lattedb.base.utilities.blackmagicsorcery import metamorph
from lattedb.base.utilities.blackmagicsorcery import concludo_expressum
from lattedb.base.models import Base


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


def get_tree(
    base: Optional[Base],
    tree: Optional[Dict[str, Base]] = None,
    todo: Optional[List[Tuple[str, Base]]] = None,
) -> Dict[str, Base]:
    """
    """
    tree = tree or {}
    if base is not None:
        todo = []
        col = None
        cls = base
    else:
        col, cls = todo.pop(0)
        tree[col] = cls

    tasks = iter_tree(col, cls)
    todo = tasks + todo

    return tree, todo


def convert_tree(flat_tree: Dict[str, Base]) -> Dict[str, Any]:
    """
    """
    flat_tree
    tree = {}

    subtree = tree
    for col in cols.split(".")[:-1]:
        subtree = subtree.setdefault(col, {})
    subtree[cols[-1]] = cls

    return tree


def iter_tree(name: str, base: Base) -> List[Tuple[str, str]]:
    """
    """
    tasks = []

    for field in base.get_open_fields():
        if isinstance(field, models.ForeignKey):
            tasks.append((f"{name}.{field.name}", field.related_model))

    return tasks
