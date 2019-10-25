#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    """Launches the web app.
    """
    for cmd in ["startapp", "makemigrations", "migrate", "runserver", "test"]:
        if cmd in sys.argv:
            raise KeyError(
                "You must use the project `manage.py` insetead of"
                f" `espressodb` file to use {cmd}."
            )

    options = {
        "DEBUG": True,
        "INSTALLED_APPS": ["espressodb.management"],
        "LOGGING": {
            "version": 1,
            "disable_existing_loggers": False,
            "handlers": {
                "console": {"level": "INFO", "class": "logging.StreamHandler"}
            },
            "loggers": {
                "espressodb": {
                    "handlers": ["console"],
                    "level": "DEBUG",
                    "propagate": True,
                }
            },
        },
    }
    try:
        from django.conf import settings
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    settings.configure(**options)
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
