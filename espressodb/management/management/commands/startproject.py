"""Overrides default startproject command to match new folder layout
"""
import os
import logging

from django.core.management.commands.startproject import Command as StartProjectCommand
from django.core.management.utils import get_random_secret_key

from espressodb.management.utilities.files import ESPRESSO_DB_ROOT


LOGGER = logging.getLogger("espressodb")


class Command(StartProjectCommand):
    """Start a new project.

    See also :data:`espressodb.management.utilities.settings.ROOT_DIR` and
    :data:`espressodb.management.utilities.settings.PROJECT_NAME`

    The default project layout is (see also the templates.)

    .. code::

        {ROOT_DIR}/
        |-- manage.py
        |-- db-config.yaml
        |-- settings.yaml
        |-- setup.py
        |-- {PROJECT_NAME}/
            |-- __init__.py
            |-- config/
                |-- __init__.py
                |-- settings.py
                |-- tests.py
                |-- urls.py
                |-- wsgi.py
                |-- migrations/
                    |-- __init__.py
                    |-- notifications/
                        |-- __init__.py
                        |-- 0001_initial.py

    Important:
        EspressoDB requires this layout for import statements and static/template path
        finding.

    Note:
        This command overrides default startproject command to match new folder layout.
    """

    help = (
        "Creates a espressodb project directory structure for the given project "
        "name in the current directory or optionally in the given directory."
    )

    rewrite_template_suffixes = (
        (".py-tpl", ".py"),
        (".yaml-tpl", ".yaml"),
        (".md-tpl", ".md"),
        (".txt-tpl", ".txt"),
    )

    def handle(self, **options):
        """Installs app in `espressodb`
        """
        options["template"] = os.path.join(
            ESPRESSO_DB_ROOT, "espressodb", "management", "templates", "project"
        )
        directory = options.get("directory") or os.getcwd()
        name = options.get("name")

        LOGGER.info("Setting up new project `%s` in `%s`", name, directory)

        options["secret_key"] = get_random_secret_key()

        options["extensions"] += ["md", "yaml"]
        settings_dir = os.path.join(directory, name)
        options["db_name"] = os.path.join(settings_dir, name + "-db.sqlite")

        super().handle(**options)

        LOGGER.info(
            "-> Creating `db-config.yaml` in the project root dir `%s`", settings_dir
        )
        LOGGER.info("   Adjust this file to establish a connection to the database")
        LOGGER.info(
            "-> Creating `settings.yaml`. Adjust this file to include later apps"
        )

        LOGGER.info("-> Done!")
        LOGGER.info("-> You can now:")
        LOGGER.info("     1a. Migrate models by running `python manage.py migrate`")
        LOGGER.info(
            "     1b. and launch a web app by running `python manage.py runserver`"
        )
        LOGGER.info(
            "     2. Add new models using `python manage.py startapp {APP_NAME}`"
        )
        LOGGER.info(
            "     3. Run `python -m pip install [--user] [-e] .`"
            " in the project root directory to add your package to your python path."
            "\n        See also `%s`.",
            os.path.join(settings_dir, "setup.py"),
        )
