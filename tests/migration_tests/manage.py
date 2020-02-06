#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from espressodb import init as _init

APP_ID = None


def main():
    """Initializes the module as standalone package without settings file.
    """

    CWD = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

    PROJECT_APPS = [f"migration_states.app{APP_ID}"] if APP_ID is not None else []
    _init(
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": f"migration-tests-db-state"
                + (f"-{APP_ID}" if APP_ID is not None else "")
                + ".sqlite",
            }
        },
        INSTALLED_APPS=PROJECT_APPS
        + [
            "espressodb.base",
            "espressodb.management",
            "django.contrib.auth",
            "django.contrib.contenttypes",
        ],
        PROJECT_APPS=PROJECT_APPS,
        ROOT_DIR=CWD,
        PROJECT_NAME="migration_states",
    )
    os.environ["ESPRESSODB_INIT_CHECKS"] = "0"  # Do not run checks for manage.py

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
