"""Prepares the usage of the lattedb app
"""
import os
from django import setup as _setup


def init():
    """Initializes the django environment for lattedb
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lattedb.config.settings")
    _setup()
