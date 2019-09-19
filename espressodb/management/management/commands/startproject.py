"""Overrides default startapp command to match new folder layout
"""
import os
import logging

import yaml

from django.core.management.commands.startproject import Command as StartProjectCommand
from django.core.management.utils import get_random_secret_key

from espressodb.management.utilities.files import ESPRESSO_DB_ROOT


LOGGER = logging.getLogger("espressodb")


class Command(StartProjectCommand):
    """Start a new project in the current or specified directory
    """

    help = (
        "Creates a espressodb project directory structure for the given project "
        "name in the current directory or optionally in the given directory."
    )

    rewrite_template_suffixes = ((".py-tpl", ".py"), (".yaml-tpl", ".yaml"))

    def handle(self, **options):
        """Installs app in `espressodb`
        """
        options["template"] = os.path.join(
            ESPRESSO_DB_ROOT, "espressodb", "management", "templates", "project"
        )
        directory = options.get("directory") or os.getcwd()
        name = options.get("name")
        print(options)

        super().handle(**options)

        settings_file = os.path.join(directory, name, "settings.yaml")
        with open(settings_file, "r") as fin:
            settings = yaml.safe_load(fin.read())

        settings["SECRET_KEY"] = get_random_secret_key()

        with open(settings_file, "w") as fout:
            fout.write(yaml.dump(settings))
