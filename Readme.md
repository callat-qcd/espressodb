# LatteDB

Lattice QCD database interface using [Django](https://docs.djangoproject.com/en/2.2/intro/tutorial01/) as the content manager.

## Description

## Install
Install via pip
```bash
pip install [--user] [-e] .
```

## Run
1. If you start the app for the first time you must configure the database setup file `db-config.yaml`.
An example file is given by `postgres-example.yaml`. Simply adjust and copy this to `db-config.yaml`.
See also [connecting-to-the-database](https://docs.djangoproject.com/en/2.2/ref/databases/#connecting-to-the-database).

2. Next, you must create the database by running
```
lattedb makemigrations # this prepares sql
lattedb migrate   # this is sql
```
This step must be repeated each time you change tables.

3. Create a super user:
```
lattedb createsuperuser
```

4. The following command in your bash to initiate an interactive server
```
lattedb runserver
```

You can access the interface in your browser.

## Development
Table schemas are implemented in `lattedb.django.base.modeles`.
See also [the Django model doc](https://docs.djangoproject.com/en/2.2/topics/db/models/).

## Management interface
Go to the admin page [http://127.0.0.1:8000](http://127.0.0.1:8000) (once the server is running.)
Note that the address might change (look at the output of `lattedb runserver`).

## Authors
* [@cchang5](https://github.com/cchang5)
* [@ckoerber](https://github.com/ckoerber)

## Contribute
To be discussed...
