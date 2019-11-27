"""Prepares the usage of the espressodb_tests module
"""
import os
from django import setup as _setup


def _init():
    """Initializes the django environment for espressodb_tests
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "espressodb_tests.config.settings")
    _setup()


_init()
