"""Functions for identifying files relevant for EspressoDB.
"""
from typing import Dict
from typing import Any

import os
import logging

import yaml

from django.core.exceptions import ImproperlyConfigured

LOGGER = logging.getLogger("espressodb")


def get_project_settings(root_dir: str) -> Dict[str, Any]:
    """Reads the settings file for given project and performs checks.

    Expects to find the keys ``SECRET_KEY``, ``DEBUG``, ``ALLOWED_HOSTS`` and
    ``PROJECT_APPS``.

    Args:
        root_dir: The root directory of the project.

    Returns:
        Settings found in settings file.

    Raises:
        ImproperlyConfigured: If not all of the essential keys are set.
    """

    settings_file = os.path.join(root_dir, "settings.yaml")

    if not os.path.exists(settings_file):
        raise ImproperlyConfigured(
            f"Was not able to find the `settings.yaml` file in directory `{root_dir}`."
            " This file is required to run the espressodb app."
        )

    with open(settings_file, "r") as fin:
        settings = yaml.safe_load(fin.read())

    for key in ["SECRET_KEY", "DEBUG", "ALLOWED_HOSTS", "PROJECT_APPS"]:
        if key not in settings:
            raise ImproperlyConfigured(
                f"The EspressoDB depends on you setting the '{key}' value"
                f" in the `settings.yaml` file. Searched in directory `{root_dir}`"
                f" but only found keys: {settings.keys()}"
            )

    return settings


def get_db_config(root_dir: str) -> Dict[str, str]:
    """Reads the db settings file for given project and performs checks.

    Expects to find the keys ``ENGINE`` and ``NAME``.

    Args:
        root_dir: The root directory of the project.

    Returns:
        Database settings found in settings file.

    Raises:
        ImproperlyConfigured: If not all of the essential keys are set.
    """

    db_config_file = os.path.join(root_dir, "db-config.yaml")

    if not os.path.exists(db_config_file):
        raise ImproperlyConfigured(
            f"Was not able to find the `db-config.yaml` file in directory `{root_dir}`."
            " This file is required to run the espressodb app."
        )

    with open(db_config_file, "r") as fin:
        db_config = yaml.safe_load(fin.read())

    if "ENGINE" not in db_config:
        raise KeyError(
            "The espressodb depends on you setting the 'ENGINE' argument"
            f" in the `db-config.yaml` file. Searched in directory `{root_dir}`"
            f" Here is a list of available keys: {db_config.keys()}"
        )

    if "NAME" not in db_config:
        raise KeyError(
            "The espressodb depends on you setting the 'NAME' argument"
            f" in the `db-config.yaml` file. Searched in directory `{root_dir}`"
            f" Here is a list of available keys: {db_config.keys()}"
        )

    return db_config


#: Root directory of the EspressoDB installation
ESPRESSO_DB_ROOT = os.path.abspath(
    os.path.join(os.path.realpath(__file__), os.pardir, os.pardir, os.pardir, os.pardir)
)
