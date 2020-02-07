"""Checks for the state of local migration files and models compared to database
"""
from espressodb.management.checks.migrations import run_migration_checks


def run_all_checks():
    """Runs all checks and raises check specific error in case script fails

    The order of checks are:
        1. :py:meth:`espressodb.management.checks.migrations.run_migration_checks`
    """
    run_migration_checks()
