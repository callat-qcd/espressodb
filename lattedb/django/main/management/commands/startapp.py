"""Overrides default startapp command to match new folder layout
"""
import os

from django.core.management.commands.startapp import Command as StartAppCommand
from lattedb.django.main.settings import BASE_DIR


class Command(StartAppCommand):
    """Start a new application in the project base dir
    """

    def handle(self, **options):
        """Installs app in `lattedb.django`
        """
        directory = options.get("directory", None) or options["name"]
        options["directory"] = os.path.join(BASE_DIR, directory)
        os.makedirs(os.path.join(BASE_DIR, directory))
        super().handle(**options)
