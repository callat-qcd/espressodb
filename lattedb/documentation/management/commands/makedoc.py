"""Command to build the docs.
"""

import os
import logging

from sphinx.application import Sphinx

from django.core.management.base import BaseCommand

from lattedb.config.settings import BASE_DIR


LOGGER = logging.getLogger("main.commands")


class Command(BaseCommand):
    """Start a new application in the project base dir
    """

    help = "Creates doc pages for all installed models"
    sourcedir = os.path.join(BASE_DIR, "documentation", "source")
    confdir = os.path.join(BASE_DIR, "documentation", "source")
    outputdir = os.path.join(BASE_DIR, "documentation", "source", "_build")
    doctreedir = os.path.join(BASE_DIR, "documentation", "source", "_build")
    builder = "html"

    def handle(self, *args, **options):
        """Installs app in `lattedb`
        """
        app = Sphinx(
            self.sourcedir, self.confdir, self.outputdir, self.doctreedir, self.builder
        )
        app.build()
