"""Setter for django config options."""
from typing import Dict, List, Optional

from django.core.exceptions import ImproperlyConfigured

from espressodb.management.utilities.files import read_db_config_from_yaml
from espressodb.management.utilities.files import read_project_config_from_yaml
from espressodb.management.utilities.environment import parse_project_config
from espressodb.management.utilities.environment import parse_db_config


def set_project_options(
    source: str,
    context: Dict,
    keys: List[str] = ("SECRET_KEY", "PROJECT_APPS", "ALLOWED_HOSTS", "DEBUG"),
    fail_on_duplicate: bool = True,
    environment_kwargs: Optional[Dict] = None,
):
    """Add database entry to context."""
    duplicate_keys = [key for key in keys if key in context]
    if duplicate_keys and fail_on_duplicate:
        raise ImproperlyConfigured(
            f"Trying to load settings from {source} which are already configured."
            f" Duplicate keys: {duplicate_keys}"
        )

    if source == "environment":
        environment_kwargs = environment_kwargs or dict()
        try:
            options = parse_project_config(keys=keys, **environment_kwargs)
        except Exception as e:
            raise ImproperlyConfigured(
                "Failed to parse settings from environment." f"Details: {e}"
            )
    elif source.endswith(".yaml") or source.endswith(".yml"):
        try:
            options = read_project_config_from_yaml(source, keys=keys)
        except Exception as e:
            raise ImproperlyConfigured(
                "Failed to parse settings from yaml." f"Details: {e}"
            )
    elif source is None:
        options = dict()
    else:
        raise ImproperlyConfigured(
            "Could not identify source for project DB."
            " Allowed options are `.yaml` files or 'environment'."
        )

    context.update(options)


def set_db_options(
    source: str,
    context: Dict,
    database: str = "default",
    environment_kwargs: Optional[Dict] = None,
):
    """Add database entry to context."""
    if source == "environment":
        environment_kwargs = environment_kwargs or dict()
        try:
            options = parse_db_config(**environment_kwargs)
        except Exception as e:
            raise ImproperlyConfigured(
                "Failed to parse db config from environment." f"Details: {e}"
            )
    elif source.endswith(".yaml") or source.endswith(".yml"):
        try:
            options = read_db_config_from_yaml(source)
        except Exception as e:
            raise ImproperlyConfigured(
                "Failed to parse db config from yaml." f"Details: {e}"
            )

    elif source is None:
        options = dict()
    else:
        raise ImproperlyConfigured(
            "Could not identify source for project DB."
            " Allowed options are `.yaml` files or 'environment'."
        )

    if database not in context:
        context[database] = options
    else:
        context[database].update(options)
