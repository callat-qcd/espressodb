"""Overrides default startapp command to match new folder layout
"""
import os
import logging

from django.core.management.commands.startproject import Command as StartProjectCommand

from espressodb.base.utilities.files import ESPRESSO_DB_ROOT


LOGGER = logging.getLogger("espressodb")


class Command(StartProjectCommand):
    """Start a new project in the current or specified directory
    """

    help = (
        "Creates a espressodb project directory structure for the given project "
        "name in the current directory or optionally in the given directory."
    )

    def handle(self, **options):
        """Installs app in `espressodb`
        """
        options["template"] = os.path.join(
            ESPRESSO_DB_ROOT, "base", "templates", "files"
        )
        super().handle(**options)
