# pylint: disable=C0413
"""Prepares the usage of the espressodb app
"""
import os
from django import setup as _setup


def init():
    """Initializes the django environment for lattedb
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "espressodb.config.settings")
    _setup()
