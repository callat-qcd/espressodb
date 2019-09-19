# How to use EspressoDB

## Description

This section explains how to use EspressoDB to create apps.
It provides a wrapper interface for [`djangos` project creation](https://docs.djangoproject.com/en/2.2/intro/tutorial01/#creating-a-project) which automatically installs EspressoDB apps.

## TL;DR
1. Create a new project: `espressodb startproject my_project; cd my_project`
    * (Optional) Configure the project infos in `db-config.yaml` and `settings.yaml`
    * (Optional) Create a new app `espressodb startapp my_app` and configure it and create new migrations
    `python manage.py makemigrations`
2. Migrate the tables to the database `python manage.py migrate`
    * (Optional) Launch a local web server `python manage.py runserver`
    * (Optional) Install your project locally  `pip install --user -e .`

## Details

### Start a project
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

The `db-config.yaml` provide the `default` database option.
As a start, they use a `sqlite` database.
You can specify different options like a `postgres` model in here (see also the [docs](https://docs.djangoproject.com/en/dev/ref/settings/#databases)).

### Create tables
At fist you have to migrate the existing models (create or update tables in the database)
```bash
python manage.py migrate
```
After this, you can already use your new app.

### Introduce new tables


### Install the module
