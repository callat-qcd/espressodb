"""This tests the first migration state where all migrations are up to date with models
and all migrations are applied to the db.
"""
from unittest import TestCase, main

from espressodb.management.checks.migrations import check_model_state
from espressodb.management.checks.migrations import check_migration_state


from .setup import ProjectSetup


class MigrationTest(ProjectSetup, TestCase):
    """Checks migrations and database states for first scenario
    """

    app_id = 1

    @staticmethod
    def test_01_check_model_state():
        """Checks if all model fields agree with all migrations
        """
        check_model_state()

    @staticmethod
    def test_02_migration_state():
        """Checks if all migrations agree with database state
        """
        check_migration_state()


if __name__ == "__main__":
    main()
