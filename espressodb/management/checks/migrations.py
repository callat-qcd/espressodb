"""Cross checks for local migrations and models compared to state of database

Notes:
    ./manage.py showmigrations is able to list non-applied migrations
    ./manage.py makemigrations is able to detect changes to models not captured by db
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
        self, state_type: str, data: Optional[Dict[str, List[str]]] = None,
    ):
        """Initialize MigrationStateError and prepares custom error method.

        Arguments:
            state_type: What is the reason for raising the error?
                E.g., changes, conflicts, ...
            data: Dictionary where keys are app names and values are migration names.
        """
        data = data or {}

        messages = [f"Migration state error: {state_type}."]
        for app, names in data.items():
            if names:
                sub_msg = f"{app}:\n\t- "
                sub_msg += "\n\t- ".join([str(name) for name in names])
                messages.append(sub_msg)

        message = "\n".join(messages)

        super().__init__(message)

        self.data = data
        self.state_type = state_type


def check_model_state():
    """Checks if the state of local models is represented by migration files.

    This code follows the logic of Djangos makemigrations
    https://github.com/django/django/blob/master/
        django/core/management/commands/makemigrations.py

    Raises:
        MigrationStateError: If the loader detects conflicts or unapplied changes.

    Future:
        It might be desirable to allow partial checks by, e.g., providing an app_labels
        argument.

    Todo:
        Tests fail if migration conflict and fail in model conflict
    """

    try:
        # Load the current graph state. Pass in None for the connection so
        # the loader doesn't try to resolve replaced migrations from DB.
        loader = MigrationLoader(None, ignore_no_migrations=True)

        # Identify conflicting apps
        conflicts = loader.detect_conflicts()
        if conflicts:
            raise MigrationStateError("conflicting migrations", conflicts)

        # Set up autodetector
        autodetector = MigrationAutodetector(
            loader.project_state(), ProjectState.from_apps(apps),
        )

        # Detect changes
        changes = autodetector.changes(graph=loader.graph)
        if changes:
            raise MigrationStateError(f"migrations have changed", changes)

    except Exception as error:
        raise MigrationStateError(
            f"error when checking state of migrations conflicts: {error}"
        )


def check_migration_state():
    """Checks if the state of local migrations is represented by the database.

    This code follows the logic of Djangos showmigrations
    https://github.com/django/django/blob/master/
        django/core/management/commands/showmigrations.py

    Raises:
        MigrationStateError: If the loader detects conflicts or unapplied changes.

    Future:
        It might be desirable to allow partial checks by, e.g., providing an app_labels
        argument.
    """
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

    if loader.applied_migrations != plan:
        data = {
            "The DB is ahead of your tables by": loader.applied_migrations.difference(
                plan
            ),
            "Your tables are ahead of the DB by": plan.difference(
                loader.applied_migrations
            ),
        }
        raise MigrationStateError(
            "applied migrations do not match local migration files", data
        )
