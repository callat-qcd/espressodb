"""Setup module for migration state test cases.
"""
import os

from espressodb import init


ROOT_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))


class ProjectSetup:  # pylint: disable=R0903
    """Class which sets up the project for unitt tests
    """

    app_id = None

    @classmethod
    def setUpClass(cls):  # pylint: disable=C0103
        """Sets up project settings.
        """
        if not cls.app_id:
            raise ValueError("You must set the app id before running the test.")
        PROJECT_APPS = [f"migration_states.app{cls.app_id}"]
        init(
            DATABASES={
                "default": {
                    "ENGINE": "django.db.backends.sqlite3",
                    "NAME": os.path.join(
                        ROOT_DIR, f"migration-tests-db-state-{cls.app_id}.sqlite"
                    ),
                }
            },
            INSTALLED_APPS=PROJECT_APPS
            + [
                "espressodb.base",
                "espressodb.management",
                "django.contrib.auth",
                "django.contrib.contenttypes",
            ],
            PROJECT_APPS=PROJECT_APPS,
            ROOT_DIR=ROOT_DIR,
            PROJECT_NAME="migration_states",
        )
