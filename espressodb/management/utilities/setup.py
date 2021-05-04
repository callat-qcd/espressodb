"""Setter for django config options."""
from typing import Dict, List, Optional

from django.core.exceptions import ImproperlyConfigured

from espressodb.management.utilities.files import read_db_config_from_yaml
from espressodb.management.utilities.files import read_project_config_from_yaml
from espressodb.management.utilities.environment import parse_project_config
from espressodb.management.utilities.environment import parse_db_config


def set_settings(
    source: str,
    context: Dict,
    keys: List[str] = ("SECRET_KEY", "PROJECT_APPS", "ALLOWED_HOSTS", "DEBUG"),
    fail_on_duplicate: bool = True,
    environment_prefix: Optional[str] = None,
):
    """Add database entry to context."""
    duplicate_keys = [key for key in keys if key in context]
    if duplicate_keys and fail_on_duplicate:
        raise ImproperlyConfigured(
            f"Trying to load settings from {source} which are already configured."
            f" Duplicate keys: {duplicate_keys}"
        )

    if source == "environment":
        try:
            environment_prefix = environment_prefix or ""
            options = parse_project_config(prefix=environment_prefix, keys=keys)
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


def set_db_config(
    source: str,
    context: Dict,
    database: str = "default",
    environment_prefix: Optional[str] = None,
):
    """Add database entry to context."""
    if source == "environment":
        try:
            environment_prefix = environment_prefix or ""
            options = parse_db_config(prefix=environment_prefix)
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


def validate_settings(context: Dict):
    for key in ["SECRET_KEY", "DEBUG", "ALLOWED_HOSTS", "PROJECT_APPS"]:
        if key not in context:
            raise ImproperlyConfigured(
                f"The EspressoDB depends on you setting the '{key}' value."
            )


def validate_db_config(databases: Dict):
    for db, db_config in databases.items():
        if "ENGINE" not in db_config:
            raise KeyError(
                f"The espressodb depends on you setting the 'ENGINE' argument for db {db}."
                f" Here is a list of available keys: {db_config.keys()}"
            )

        if "NAME" not in db_config:
            raise KeyError(
                f"The espressodb depends on you setting the 'NAME' argument for db {db}."
                f" Here is a list of available keys: {db_config.keys()}"
            )
