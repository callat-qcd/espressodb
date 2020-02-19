# How to use EspressoDB

This section explains how to use EspressoDB to create projects and apps.
It provides a wrapper interface for [`djangos` project creation](https://docs.djangoproject.com/en/dev/intro/tutorial01/#creating-a-project) which streamlines the creation process.

## TL;DR
1. [Install EspressoDB](#install-espressodb)
2. [Create a new project](#start-a-project)
    ```bash
    espressodb startproject my_project
    ```
    The following commands must be run in the project root directory:
    ```bash
    cd my_project
    ```
3. _(Optional)_ [Update the configurations of the project](#configure-your-project) in `db-config.yaml` and `settings.yaml`
4. _(Optional)_ [Create a new app](#create-a-new-app)
    ```bash
    python manage.py startapp my_app
    ```
    configure it and [create new migrations](#create-migrations)
    ```bash
    python manage.py makemigrations
    ```
5. [Create or update the tables](#migrate-changes)
    ```bash
    python manage.py migrate
    ```
6. _(Optional)_ [Launch a local web app](#launch-a-local-web-app)
    ```bash
    python manage.py runserver
    ```
7. _(Optional)_ [Install your project locally](#install-your-project-locally) to use it in other modules
    ```
    pip install [--user] [-e] .
    ```

For more details how to customize your project, take a look at the [how to create the example project](example/project-creation/index) guide.

## Details

### Install EspressoDB
You can pip install this package by running
```bash
pip install [--user] espressodb
```

You can also install the project from source
```bash
git clone https://www.github.com/callat-qcd/espressodb.git
cd espressodb
pip install [--user] [-e] .
```

### Start a project
A project is the core module which manages the settings for your (future) tables like connections to the database, security levels and so on.

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
        |-- tests.py
        |-- urls.py
        |-- wsgi.py
        |-- migrations/
            |-- __init__.py
            |-- notifications/
                |-- __init__.py
                |-- 0001_initial.py
```

<div class="admonition note">
<p class="admonition-title">Note</p>
<p>EspressoDB makes use of the project structure by, e.g., finding import paths and static files.
Thus, unless you know what you are doing, it is recommended to stick to this folder layout.</p>
</div>

### Configure your project

The `settings.yaml` and `db-config.yaml` are convenience files for easy updates (without accidentally committing secret passwords).
Both of them may contain passwords (`SECRET_KEY` in the `settings` and database `PASSWORD` in the db config) and thus you should pay attention if or with whom you want to share them.

The `db-config.yaml` provides the `default` database option
```
ENGINE: django.db.backends.sqlite3
NAME: /path/to/project/my_project/my-project-db.sqlite
```
The first option specifies the database backend.
As default, it uses the file based `sqlite` database.
For this case, the name points to the absolute path of the file (which allows interface for external apps).
You can specify different database options like a `postgres` model in this file (see also the [docs](https://docs.djangoproject.com/en/dev/ref/settings/#databases)).

The `settings.yaml` specifies the database encryption, which [apps](#create-a-new-app) your projects will use and, in case you want to, how you want to run the web server
```
SECRET_KEY: "Sup3r_compl1cated-P4ssw0rd!"
PROJECT_APPS: []
ALLOWED_HOSTS: []
DEBUG: True
```
Both files are needed and eventually imported by `my_project/my_project/config/settings.py`.
If you want to learn more or have different setups, feel free to adjust this file with help of the [settings documentation](https://docs.djangoproject.com/en/dev/ref/settings/).


### Create or update the database
After you have created a project for the first time, you have to initialize your tables.
Django provides an interface to manage the communication with the database without you running any SQL commands directly.
Specifically, you can program Python classes, which specify a given table layout, and know how to talk to a database.
This concept is called Object-Relational Mapping (ORM).
These classes are called models and have a one-to-one correspondence to tables within the database.
By default Django provides a few basic models like the `User` class.

Updating the database with new tables or modifying old ones is a crucial step.
If the Python backend encounters tables which do not match what the user specified, this could cause the ORM to fail.
To ensure table and code updates are executed in a consistent way Django, implements the following two-step procedure:

#### Create migrations
Once the Python models have been updated, Django identifies a strategy how the existing tables within the DB must be adjusted to match the new specifications.
E.g., if a column was added, how to populate old entries which did not have this column yet.
If a change is implemented which needs user input, Django will ask you how to proceed.
This update strategy will be summarized in a `migration` file.
You start this procedure by running
```
python manage.py makemigrations
```
In this step, the database is not modified.
So if this step fails, nothing crucial has happened yet.
However you should make sure that before continuing, everything works as expected.

#### Migrate changes
To update the database, you have to `migrate` changes.
This applies the specifications in the `migration` files and alters your database.
To apply the migrations run
```bash
python manage.py migrate
```

After successfully migrating new or updated models, you are good to go and can for example [launch a web app](#launch-a-local-web-app).

For further [migration strategies, see also the Django docs](https://docs.djangoproject.com/en/dev/topics/migrations/).

### Launch a local web app
Django provides an easy interface to launch a local web server.
Once you project is set up, you can run
```
python manage.py runserver
```
to start a local lightweight server which runs by default on localhost: [http://127.0.0.1:8000/](http://127.0.0.1:8000/).
EspressoDB provides default views, meaning once your tables have been successfully migrated, you can directly see your project home page.
Everyone who has access to this port on your machine can access the launched web page.
This means, by default, you are the only one able to see it.

### Create a new app
Apps are submodules within your project and implement new tables and other features.
To start a new app, run the following command
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

<div class="admonition note">
<p class="admonition-title">Note</p>
<p>
    EspressoDB makes use of the project and app structure by, e.g., finding import paths and static files.
    Thus, unless you know what you are doing, it is recommended to stick to this folder layout.
</p>
</div>


To let your project know that it also has to include the new app, change the `settings.yaml` to also include
```
PROJECT_APPS:
    - my_project.my_app
```

Because the project is empty, nothing significant has changed thus far.

To implement your first table, you must adjust the app models.
E.g., to create a table which works with the EspressoDB default features, update `my_project/my_app/models.py` to
```python
from django.db import models
from espressodb.base.models import Base

class MyTable(Base):
    i = models.IntegerField(help_text="An important integer")
```
This implements a new model with the default columns provided by the EspressoDB base model (e.g., `user`, `last_modified`, `tag`) and adds an integer column called `i`.
You can find more information about tables in EspressoDB in our [example project](example/project-creation/app-creation.md) or take a look at the [Django models documentation](https://docs.djangoproject.com/en/dev/topics/db/models/) for a complete reference.

<div class="admonition note">
<p class="admonition-title">Note</p>
<p>
    Note that you have to replace <code>models.Model</code> with EspressoDB's <code>Base</code>. <code>Base</code> derives from Django's default <code>models.Model</code> but provides further features needed by EspressoDB.
</p>
</div>

To update your database you have to (again) [create and migrate `migrations`](#create-or-update-the-database).
```bash
python manage.py makemigrations
python manage.py migrate
```
After this, you should be able to see a  _My Table_  entry within the documentation
```bash
python manage.py runserver
```
and visit [http://127.0.0.1:8000/documentation/my_app/](http://127.0.0.1:8000/documentation/my_app/).


### Install your project locally
The easiest way to let your other Python modules use these tables is to install your project as a pip module (not on Python package index, just in your local path).
To do so, take a look at `setup.py`, [adjust it to your means](https://docs.python.org/3.7/distutils/setupscript.html) and run
```
python -m pip install [--user] [-e] .
```
The `[-e]` options symlinks the install against this folder and can be useful incase you want to continue updating this module, e.g., for development purposes.

That's it.

You can now use your tables in any Python program like
```python
from my_project.my_app.models import MyTable

all_entries = MyTable.objects.all()

for entry in all_entries:
    print(entry, entry.tag)
```
See also the [Django query docs](https://docs.djangoproject.com/en/dev/topics/db/queries/) for more sophisticated options.
