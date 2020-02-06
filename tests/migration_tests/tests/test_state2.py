"""This tests the second migration state where not all migrations are up to date with
models but all migrations are applied to the db.
"""
from unittest import TestCase, main

from espressodb.management.checks.migrations import MigrationStateError
from espressodb.management.checks.migrations import check_model_state
from espressodb.management.checks.migrations import check_migration_state


from .setup import ProjectSetup


class MigrationTest(ProjectSetup, TestCase):
    """Checks migrations and database states for second scenario
    """

    app_id = 2

    def test_01_check_model_state(self):
        """Checks if all model fields agree with all migrations
        """
        with self.assertRaises(MigrationStateError):
            check_model_state()

    @staticmethod
    def test_02_migration_state():
        """Checks if all migrations agree with database state
        """
        check_migration_state()


if __name__ == "__main__":
    main()
