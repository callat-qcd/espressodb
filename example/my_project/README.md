# Example project

This folder contains an example project for `EspressoDB`.
It contains a minimal table layout and custom views.


## How to use it

First, you must create a local database.
This is done by running
```bash
python manage.py migrate
```
in this directory.
This populates the database with empty tables.

To populate tables, you can run the `add_data.py` script.
After this, you can start the web app and take a look around.

If you want to see the admin pages, you must create a (superuser) account first.
This is done by running
```bash
python manage.py createsuperuser
```
The password will be encrypted and stored in the database `my_project.sqlite`.

After this, you can launch the webapp by typing
```bash
python manage.py runserver
```
and visit [http://127.0.0.1:8000](http://127.0.0.1:8000).
