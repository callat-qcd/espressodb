Summary of EspressoDB functionality
====================================

URLs
-----

If you have created you project using EspressoDB, the default project url config includes the app url name spaces as

.. code::

    urlpatterns = [
        path("", include("espressodb.base.urls", namespace="base")),
        path("admin/", admin.site.urls),
        path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
        path("logout/", auth_views.LogoutView.as_view(), name="logout"),
        path(r"documentation/", include("espressodb.documentation.urls", namespace="documentation")),
        path(r"notifications/", include("espressodb.notifications.urls", namespace="notifications")),
    ]


**Module**: :mod:`espressodb.base.urls`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: espressodb.base.urls
    :members:
    :noindex:
    :special-members:


**Module**: :mod:`espressodb.documentation.urls`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: espressodb.documentation.urls
    :members:
    :noindex:
    :special-members:


**Module**: :mod:`espressodb.notifications.urls`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: espressodb.notifications.urls
    :members:
    :noindex:
    :special-members:


Templatetags
-------------

**Module**: :mod:`espressodb.base.templatetags.base_extras`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: espressodb.base.templatetags.base_extras
    :members:
    :noindex:
    :special-members:


**Module**: :mod:`espressodb.documentation.templatetags.documentation_extras`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. automodule:: espressodb.documentation.templatetags.documentation_extras
    :members:
    :noindex:
    :special-members:


**Module**: :mod:`espressodb.notifications.templatetags.notifications_extras`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule::espressodb.notifications.templatetags.notifications_extras
    :members:
    :noindex:
    :special-members:
