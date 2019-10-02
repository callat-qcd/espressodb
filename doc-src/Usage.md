# How to use EspressoDB

## Description

This section explains how to use EspressoDB to create apps.
It provides a wrapper interface for [`djangos` project creation](https://docs.djangoproject.com/en/2.2/intro/tutorial01/#creating-a-project) which automatically installs EspressoDB apps.

## TL;DR
1. Create a new project: `espressodb startproject my_project; cd my_project`
    * (Optional) Configure the project infos in `db-config.yaml` and `settings.yaml`
    * (Optional) Create a new app `python manage.py startapp my_app` and configure it and create new migrations
    `python manage.py makemigrations`
2. Migrate the tables to the database `python manage.py migrate`
    * (Optional) Launch a local web server `python manage.py runserver`
    * (Optional) Install your project locally  `pip install --user -e .`

## Details

### Start a project
A project is the root module which manages the settings for your (future) tables like connections to the database, security levels and so on.

You can initialize an empty project by running

```bash
espressodb startproject my_project
```

This will create the following folder structure

```bash
my_project/
|-- manage.py
|-- db-config.yaml
|-- settings.yaml
|-- setup.py
|-- my_project/
    |-- __init__.py
    |-- config/
        |-- __init__.py
        |-- settings.py
        |-- urls.py
        |-- wsgi.py
```

The `settings.yaml` and `db-config.yaml` are convenience files which are imported in the `settings.py` file.
Both of them may contain passwords (`SECRET_KEY` in the `settings` and database `PASSWORD` in the db config) and thus you should pay attention if or with whom you want to share them.

The `db-config.yaml` provides the `default` database option.
As a start, it uses a `sqlite` database.
You can specify different options like a `postgres` model in here (see also the [docs](https://docs.djangoproject.com/en/dev/ref/settings/#databases)).

### Create the database and tables
After you have created a project for the first time, you have to initialize your tables.
Django provides an interface to manage the communication with the database without you running any SQL commands directly.
Specifically, you can program python classes, which specify a given table layout, and know how to talk to a database.
These classes are called models and have a one-to-one correspondence to tables within the database.
By default django provides a few basic models like the `User` class.

Updating the database with new tables or modifying old ones is a crucial step.
If the python backend encounters tables which do not match what the user specified, this could cause the ORM to fail.
To ensure table and code updates are executed in a consistent way django implements the following two-step procedure:

1. Once the python models have been updated, django identifies a strategy how the existing tables within the DB must be adjusted to match the new specifications.
E.g., if a column was added, how to populate old entries which did not have this column.
In this step, the database is not touched yet and `migration` files are created.
You start this procedure by running
```
python manage.py makemigrations
```
If this fails, nothing crucial has happend yet.
However you should make sure that before continuing, everything works as expected.

2. To update the database, you have to `migrate` changes.
This applies the specifications in the `migration` files and alters your database.
To apply the migrations run
```bash
python manage.py migrate
```

After successfully migrating new or updated models, you can start using your project by, e.g., launching the web interface:
```bash
python manage.py runserver
```

### Create a new app
To start a new app, the sub module for new tables, run the following command
```bash
python manage.py startapp my_app
```

This will create the new folders and files
```bash
my_project/
|-- my_app/
    |-- __init__.py
    |-- admin.py
    |-- apps.py
    |-- models.py
    |-- tests.py
    |-- views.py
    |-- templates/
    |-- migrations/
        |-- __init__.py
```

To let your project know that it also has to run the new app, change the `settings.yaml` to also include
```
PROJECT_APPS:
    - my_project.my_app
```

Because the project is empty, nothing significant has changed thus far.

To implement your first table, you must adjust the models file.
E.g., to create a table which works with the `EspressoDB` default features, update `my_app/models.py` to
```python
from espressodb.base.models import Base

class MyTable(Base):
    pass
```
This implements a new model with the default columns provided by the `EspressoDB` base model (e.g., `user`, `last_modified`,  `tag`, `type`, `misc`).


To update your database you have to (again) create and migrate `migrations`.
```bash
python manage.py makemigrations
python manage.py migrate
```

After this, you should be able to see a  _My Table_  entry within the documentation
```bash
python manage.py runserver
```
and visit [http://127.0.0.1:8000/documentation/my_app/](http://127.0.0.1:8000/documentation/my_app/).

For implementing more sophisticated tables, see also the [django model documentation](https://docs.djangoproject.com/en/2.2/topics/db/models/).

>>> Note that you have to replace `models.Model` with `EspressoDB`s `Base`.
    `Base` derives from django's default `models.Model` but provides further features needed by `EspressoDB`.

### Using your models in external modules
The easiest way to let your other python modules use these tables is to install your project as a pip moduel (not on a python index page, just in your local path).
To do so take a look at `setup.py`, adjust it to your means and run
```
python -m pip install [--user] [-e] .
```
The `[-e]` options symlinks the install against this folder and can be useful incase you want to continue updating this module, e.g., for development purposes.
That's it.
You can now use your tables in any python program like
```python
from my_project.my_app.models import MyTable

all_entries = MyTable.objects.all()

for entry in all_entries:
    print(entry, entry.tag)
```
See also the [django query docs](https://docs.djangoproject.com/en/2.2/topics/db/queries/) for more sophisticated options.
