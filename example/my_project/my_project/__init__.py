"""Prepares the usage of the my_project module
"""
import os
from django import setup as _setup


def _init():
    """Initializes the django environment for my_project
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_project.config.settings")
    _setup()


_init()
