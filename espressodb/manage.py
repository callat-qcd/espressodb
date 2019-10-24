#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    """Launches the web app.
    """
    for cmd in ["startapp", "makemigrations", "migrate", "runserver"]:
        if cmd in sys.argv:
            raise KeyError(
                "You must use the project `manage.py` insetead of"
                f" `espressodb` file to use {cmd}."
            )

    if "test" in sys.argv:
        example_path = os.path.join(ROOT, "example", "my_project")
        if not os.path.exists(example_path):
            raise OSError(
                "Could not locate the example project."
                f" Looked up {example_path}."
                " Are you running espressodb from the repo installation?"
            )
        sys.path.insert(0, example_path)
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_project.config.settings")
    else:
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
        except ImportError as exc:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            ) from exc

        settings.configure(**options)

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
