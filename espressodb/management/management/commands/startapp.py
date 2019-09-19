"""Overrides default startapp command to match new folder layout
"""
import os
import logging

raise NotImplementedError("Need to update module")

from django.core.management.commands.startapp import Command as StartAppCommand
from espressodb.config.settings import BASE_DIR


LOGGER = logging.getLogger("main.commands")


class Command(StartAppCommand):
    """Start a new application in the project base dir
    """

    def handle(self, **options):
        """Installs app in `espressodb`
        """
        app_name = options["name"]
        directory = options.get("directory", None) or app_name
        options["directory"] = base_dir = os.path.join(BASE_DIR, directory)
        os.makedirs(os.path.join(base_dir))
        super().handle(**options)
        LOGGER.info(
            "App `%s` was successfully created. In order to install it", app_name
        )
        LOGGER.info("1. Adjust the app (directory `%s`)", base_dir)
        LOGGER.info(
            "2. Add `%s` to the `PROJECT_APPS` in `settings.yaml`",
            f"espressodb.{app_name}",
        )
        LOGGER.info("3. Run `espressodb makemigrations`")
        LOGGER.info("4. Run `espressodb migrate`")
