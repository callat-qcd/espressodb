# LatteDB

Lattice QCD database interface using [Django](https://docs.djangoproject.com/en/2.2/intro/tutorial01/) as the content manager.

## Description

## Install
Install via pip
```bash
pip install [--user] [-e] .
```

## Run
If you start the app for the first time, run
```
python manage.py makemigrations  # this updates schemas incase changes where pushed
python manage.py migrate   # this creates the database
python manage.py createsuperuser  # this creates a superuser fo the database
```
The following command in your bash to initiate an interactive server

```
python manage.py runserver
```

You can access the interface in your browser.

## Development
Table schemas are implemented in `lattestructs.modeles`.
See also [the Django model doc](https://docs.djangoproject.com/en/2.2/topics/db/models/).

## Authors
* [@cchang5](https://github.com/cchang5)
* [@ckoerber](https://github.com/ckoerber)

## Contribute
To be discussed...
