# pylint: disable=C0413
"""Prepares the usage of the espressodb app
"""
from django import setup as _setup
from django.conf import settings


def init(**kwargs):
    """Initializes the django environment for espressodb
    """
    settings.configure(
        DEBUG=True,
        INSTALLED_APPS=[
            "espressodb.base",
            "espressodb.documentation",
            "espressodb.management",
            "django.contrib.auth",
            "django.contrib.contenttypes",
        ],
        LOGGING={
            "version": 1,
            "disable_existing_loggers": False,
            "handlers": {"console": {"level": "INFO", "class": "logging.StreamHandler"}},
            "loggers": {
                "espressodb": {
                    "handlers": ["console"],
                    "level": "DEBUG",
                    "propagate": True,
                }
            },
        },
        **kwargs
    )

    _setup()
