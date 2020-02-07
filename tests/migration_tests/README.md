# Migration tests

This app tests whether migration checks run as expected.
To make this work, the test project contains four apps with complete and incomplete migration states to trigger exceptions.

Each project app corresponds to a given state with a given migration history and database file.
E.g., the app `migration_states/app1` corresponds to the database `migration-tests-db-state-1.sqlite`.
There is no project settings file to run tests for each state individually.
Thus tests run outside the regular Django framework and treat the project as an external EspressoDB project.

## State 1

For this state, the models, migrations, and database are all up to date.
No error should be raised.

## State 2

Migrations and models are not up to date.

Migrations (`python manage.py makemigrations`) were created and applied (`python manage.py migrate`) with
```python
class A1(Base):
    i = models.IntegerField()
```
Next `A1` was updated to
```python
class A1(Base):
    i = models.IntegerField()
    j = models.IntegerField(default=1)
```
without creating migrations.

Running `check_model_state` should raise a `MigrationStateError` while `check_migration_state` should pass.

## State 3

Migrations and models are up to date but the migration files are ahead of the database.

Migrations were created (`python manage.py makemigrations`) and applied (`python manage.py migrate`) with
```python
class A1(Base):
    i = models.IntegerField()
```
Next `A1` was updated to
```python
class A1(Base):
    i = models.IntegerField()
    j = models.IntegerField(default=1)
```
and migrations were created again; without updating the database.

Running `check_model_state` should pass while `check_migration_state` should raise a `MigrationStateError` because local table definitions are ahead of the DB.

## State 4

Migrations and models are up to date but the migration files are behind the database.

Migrations were created (`python manage.py makemigrations`) and applied (`python manage.py migrate`) with
```python
class A1(Base):
    i = models.IntegerField()
```
Next `A1` was updated to
```python
class A1(Base):
    i = models.IntegerField()
    j = models.IntegerField(default=1)
```
migrations were created again, the database was updated and the migration history (as well as model) were reverted to the previous state.

Running `check_model_state` should pass while `check_migration_state` should raise a `MigrationStateError` because local table definitions are ahead of the DB.
