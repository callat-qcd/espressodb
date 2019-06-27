"""Script to completely whipe migrations.
"""
import os
import logging

from django.core.management.base import BaseCommand, CommandError
from lattedb.django.main.settings import DEBUG, PROJECT_APPS, ROOT_DIR


LOGGER = logging.getLogger("main.commands")


class Command(BaseCommand):
    """Command to earase all migrations
    """

    helps = "Whipes out all migrations"

    def handle(self, *args, **options):
        """Looks up all project apps and whipes their migrations
        """
        if DEBUG:
            for app in PROJECT_APPS:
                app_path = os.path.join(ROOT_DIR, *app.split("."), "migrations")
                LOGGER.info("Loogking into: `%s`", app_path)
                migrations = [
                    fle
                    for fle in os.listdir(app_path)
                    if fle.endswith("py") and fle != "__init__.py"
                ]
                for migration in migrations:
                    LOGGER.info("\t%s", migration)
                    os.remove(os.path.join(app_path, migration))

        else:
            raise CommandError("Only allowed to whipe migrations in development mode.")
