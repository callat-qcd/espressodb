# The private views

By default, views you create are public -- any user who has access to the address where the web page is launched, is able to see the content.
It is also possible to require the user to be logged in (and have specified permissions) to see views.

Since you have just created the database, there is no user specified.
You can create a new user by running
```
python manage.py createsuperuser
```
This information is stored (encrypted) in the database `my_project.sqlite`.

Once you have logged in, you will be able to access two more pages which are present on default:

![The login view](../../_static/example-admin-links.png)

1. The notifications page: [http://127.0.0.1:8000/notifications/](http://127.0.0.1:8000/notifications/)
2. And the admin pages: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

### The notifications page

![The home page](../../_static/example-notifications.png)


### The admin pages

![The home page](../../_static/example-admin-view.png)
![The home page](../../_static/example-admin-notifications.png)
