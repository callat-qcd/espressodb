"""
"""
import os
from unittest import TestCase, main

from espressodb import init
from espressodb.management.checks.migrations import check_model_state
from espressodb.management.checks.migrations import check_migration_state

CWD = os.path.abspath(os.path.dirname(__file__))

print(CWD)


class Test(TestCase):
    @classmethod
    def setUpClass(cls):
        PROJECT_APPS = ["migration_tests.app1"]
        init(
            DATABASES={
                "default": {
                    "ENGINE": "django.db.backends.sqlite3",
                    "NAME": "migration-tests-db-state-1.sqlite",
                }
            },
            INSTALLED_APPS=PROJECT_APPS
            + [
                "espressodb.base",
                "espressodb.management",
                "django.contrib.auth",
                "django.contrib.contenttypes",
            ],
            PROJECT_APPS=["migration_tests.app1"],
            ROOT_DIR=CWD,
            PROJECT_NAME="migration_tests",
        )

    def test_01(self):
        check_model_state()

    def test_02(self):
        check_migration_state()


if __name__ == "__main__":
    main()
