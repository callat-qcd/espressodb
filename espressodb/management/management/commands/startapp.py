"""Starting app interface for EspressoDB.
"""
import os
import logging

from django.core.management.commands.startapp import Command as StartAppCommand

from espressodb.management.utilities.settings import ROOT_DIR, PROJECT_NAME
from espressodb.management.utilities.files import ESPRESSO_DB_ROOT

LOGGER = logging.getLogger("espressodb")


class Command(StartAppCommand):
    """Start a new application in the project base dir (``ROOT_DIR/PROJECT_NAME``).

    See also :data:`espressodb.management.utilities.settings.ROOT_DIR` and
    :data:`espressodb.management.utilities.settings.PROJECT_NAME`

    The default app layout is (see also the templates.)

    .. code::

        {PROJECT_NAME}/
        |-- {APP_NAME}/
            |-- __init__.py
            |-- admin.py
            |-- apps.py
            |-- models.py
            |-- tests.py
            |-- views.py
            |-- templates/
            |-- migrations/
                |-- __init__.py

    Important:
        EspressoDB requires this layout for import statements and static/template path
        finding.

    Note:
        This command overrides default startapp command to match new folder layout.
    """

    def handle(self, **options):
        options["template"] = os.path.join(
            ESPRESSO_DB_ROOT, "espressodb", "management", "templates", "app"
        )

        app_name = options["name"]
        options["directory"] = base_dir = os.path.join(ROOT_DIR, PROJECT_NAME)
        options["project_name"] = PROJECT_NAME

        super().handle(**options)
        LOGGER.info(
            "App `%s` was successfully created. In order to install it", app_name
        )
        LOGGER.info(
            "1. Adjust the app (directory `%s%s%s`)", base_dir, os.sep, app_name
        )
        LOGGER.info(
            "2. Add `%s.%s` to the `PROJECT_APPS` in `settings.yaml`",
            PROJECT_NAME,
            app_name,
        )
        LOGGER.info("3. Run `python manage.py makemigrations`")
        LOGGER.info("4. Run `python manage.py  migrate`")
