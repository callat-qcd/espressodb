# pylint: disable=C0413
"""Initializes minimal settings to launch EspressoDB
"""
from django import setup as _setup
from django.conf import settings


def init(**kwargs):
    """Initializes minimal settings to launch EspressoDB without a project

    Launches  ``django.conf.settings.configure`` and runs ``django.setup``.
    This is needed to use EspressoDB command line tools.

    Keyword Args:
        kwargs: Kwargs are fed to ``settings.configure``.
    """
    settings.configure(
        DEBUG=True,
        INSTALLED_APPS=[
            "espressodb.base",
            "espressodb.documentation",
            "espressodb.management",
            "espressodb.notifications",
            "django.contrib.auth",
            "django.contrib.contenttypes",
        ],
        LOGGING={
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
        **kwargs
    )

    _setup()
