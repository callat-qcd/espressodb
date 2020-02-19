"""Cross checks for local migrations and models compared to state of database
"""
from typing import Dict, List, Optional

from django.apps import apps

from django.db import DEFAULT_DB_ALIAS, connections

from django.db.migrations.loader import MigrationLoader
from django.db.migrations.autodetector import MigrationAutodetector
from django.db.migrations.state import ProjectState


class MigrationStateError(Exception):
    """Error which is raised if the local state of models or migrations does not reflect
    the database.
    """

    def __init__(
        self, header: str, data: Optional[Dict[str, List[str]]] = None,
    ):
        """Initialize MigrationStateError and prepares custom error method.

        Arguments:
            header: What is the reason for raising the error?
                E.g., changes, conflicts, ...
            data: Dictionary where keys are app names and values are migration names.
        """
        data = data or {}

        messages = [header]
        for app, names in data.items():
            if names:
                sub_msg = f"{app}:\n\t- "
                sub_msg += "\n\t- ".join([str(name) for name in names])
                messages.append(sub_msg)

        message = "\n".join(messages)

        super().__init__(message)

        self.data = data
        self.header = header


def check_model_state():
    """Checks if the state of local models is represented by migration files.

    This code follows the logic of Djangos makemigrations
    https://github.com/django/django/blob/master/django/core/management/commands/makemigrations.py

    Raises:
        MigrationStateError: If the loader detects conflicts or unapplied changes.

    Future:
        It might be desirable to allow partial checks by, e.g., providing an app_labels
        argument.
    """

    try:
        # Load the current graph state. Pass in None for the connection so
        # the loader doesn't try to resolve replaced migrations from DB.
        loader = MigrationLoader(None, ignore_no_migrations=True)

        # Identify conflicting apps
        conflicts = loader.detect_conflicts()

        # Set up autodetector and detect changes
        changes = MigrationAutodetector(
            loader.project_state(), ProjectState.from_apps(apps),
        ).changes(graph=loader.graph)
    except Exception as error:
        raise MigrationStateError(
            f"Error when checking state of migrations conflicts:\n{error}"
        )

    if conflicts:
        raise MigrationStateError("Conflicting migrations", conflicts)

    if changes:
        raise MigrationStateError(f"Migrations have changed", changes)


def check_migration_state():
    """Checks if the state of local migrations is represented by the database.

    This code follows the logic of Djangos showmigrations
    https://github.com/django/django/blob/master/django/core/management/commands/showmigrations.py

    Raises:
        MigrationStateError: If the loader detects conflicts or unapplied changes.

    Future:
        It might be desirable to allow partial checks by, e.g., providing an app_labels
        argument.
    """
    try:
        connection = connections[DEFAULT_DB_ALIAS]
        loader = MigrationLoader(connection, ignore_no_migrations=True)

        graph = loader.graph
        targets = graph.leaf_nodes()

        plan = set()
        seen = set()
        # Generate the plan
        for target in targets:
            for migration in graph.forwards_plan(target):
                if migration not in seen:
                    node = graph.node_map[migration]
                    plan.add(node.key)
                    seen.add(migration)

        # Apparently Django returns {} if no connection (which is a set not a dict).
        tmp = loader.applied_migrations
        applied_migrations = set(tmp if isinstance(tmp, set) else tmp.keys())

    except Exception as error:
        raise MigrationStateError(
            f"Error when checking state of migrations conflicts:\n{error}"
        )

    if applied_migrations != plan:
        data = {
            "The DB is ahead of your tables by": applied_migrations.difference(plan),
            "Your tables are ahead of the DB by": plan.difference(applied_migrations),
        }
        raise MigrationStateError(
            "Applied migrations do not match local migration files", data
        )


def run_migration_checks():
    """Runs all migration checks at once

    In order:
        1. :py:meth:`espressodb.management.checks.migrations.check_model_state`
        2. :py:meth:`espressodb.management.checks.migrations.check_migration_state`

    Raises:
        MigrationStateError: If the loader detects conflicts or unapplied changes.
    """
    check_model_state()
    check_migration_state()
