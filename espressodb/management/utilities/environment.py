"""Submodule for parsing Django settings from environment."""
from typing import Dict, Optional, List

import logging
import os

LOGGER = logging.getLogger("espressodb")


def split_list(string: str, seperator: str = ",") -> List[str]:
    """Split and strip elements from string."""
    return [el.strip() for el in string.split(seperator)]


def map_bool(string: str):
    """Map strings to bool by mapping to ints first if numeric or comparing with 'true'."""
    return bool(int(string)) if string.isnumeric() else string.lower() == "true"


SETTINGS_PARSER = {
    "SECRET_KEY": str,
    "ALLOWED_HOSTS": split_list,
    "DEBUG": map_bool,
    "PROJECT_APPS": split_list,
}


def get_values_from_env(
    prefix: str, keys: Optional[List[str]] = None, fail_if_missing: bool = True
) -> Dict[str, str]:
    """Extract strings from environment matching."""
    options = dict()

    matches = [key for key in os.environ if key.startswith(prefix)]
    if keys:
        variables = {
            key.replace(prefix, ""): os.environ[key]
            for key in matches
            if key.replace(prefix, "") in keys
        }
    else:
        variables = {key.replace(prefix, ""): os.environ[key] for key in matches}

    if fail_if_missing and options.keys() != set(keys):
        raise KeyError(
            "Could not locate all expected environment variables."
            f" Missing: {set(keys) - options.keys()}"
        )
    return variables


def parse_db_config(prefix: str):
    """..."""


def parse_project_config(prefix: str, keys: List[str]):
    """..."""
    if not keys:
        raise KeyError(
            "Setting names must be explicitly provided by name when loading from environment."
        )
    unsupported_settings = [key for key in keys if key not in SETTINGS_PARSER]
    if unsupported_settings:
        LOGGER.warning(
            "Loading settings %s from environment assuming string type.",
            unsupported_settings,
        )

    return {
        key: SETTINGS_PARSER.get(key, str)(val)
        for key, val in get_values_from_env(prefix, keys, fail_if_missing=True).items()
    }
