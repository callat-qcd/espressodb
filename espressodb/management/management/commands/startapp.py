"""Overrides default startapp command to match new folder layout
"""
import os
import logging

from django.core.management.commands.startapp import Command as StartAppCommand

try:
    from espressodb.management.utilities.settings import ROOT_DIR, PROJECT_NAME
except ValueError:
    pass

LOGGER = logging.getLogger("espressodb")


class Command(StartAppCommand):
    """Start a new application in the project base dir
    """

    def handle(self, **options):
        """Installs app in `espressodb`

        .. note: Overwrites default directory
        """
        app_name = options["name"]
        options["directory"] = base_dir = os.path.join(ROOT_DIR, PROJECT_NAME, app_name)
        os.makedirs(os.path.join(base_dir))

        print(options)
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
