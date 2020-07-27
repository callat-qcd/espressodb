Customizing EspressoDB
======================

This section specifies your options to update EspressoDB's appearance.

Admin page
----------

By default, the :meth:`espressodb.base.admin.register_admins` method.
This method is called in each apps  :code:`admin.py`.
For example `my_project/hamiltonian/admin.py` file looks like

.. code-block:: python

    from espressodb.base.admin import register_admins

    register_admins("my_project.hamiltonian")

Adding the :code:`exclude_models` keyword argument to the method, prevents rendering models in the admin page.

This feature can be used to customize your admin view for a specific model

.. code-block:: python

    from django.contrib.admin import register, ModelAdmin
    from espressodb.base.admin import register_admins

    from my_project.hamiltonian.models import Eigenvalue

    # Render all but the Eigenvalue admin of my_project.hamiltonian using EspressoDB
    register_admins("my_project.hamiltonian", exclude_models=["Eigenvalue"])

    # Implement a custom admin for Eigenvalue
    @register(Eigenvalue)
    class NewEigenvalueAdmin(ModelAdmin):
        pass

See also the `Django admin reference <https://docs.djangoproject.com/en/dev/ref/contrib/admin/>`_ for more details

On default, EspressoDB uses :class:`espressodb.base.admin.ListViewAdmin` to render model admins.
You can change the default template by providing the ``admin_class`` keyword to :meth:`espressodb.base.admin.register_admins`.

Navigation customizations
-------------------------

On default, EspressoDB renders navigation elements like app views, the documentation, admin links and others.
It is possible to update the default rendering by `extending <https://docs.djangoproject.com/en/dev/ref/templates/language/#template-inheritance>`_ the :code:`base.html` template.

The default navigation bar is implemented in :code:`espressodb/base/templates/base.html` by the following code (suppressing the HTML tags and classes)

.. code-block:: html

    <nav>
        {% block nav %}
        <!-- Logo -->
        ...
        <ul>
            {% block nav-app-links %}
            <!-- App links -->
            ...
            {% endblock nav-app-links %}
            {% block nav-default-links %}
            <!-- Default EspressoDB links (docs, populate, notifications, admin) -->
            ...
            {% endblock nav-default-links %}
        </ul>
        <ul>
            <!-- Login/out links -->
            ...
        </ul>
        {% endblock nav %}
    </nav>

To write your custom navigation bar implementation, you have to create a new :code:`base.html` template which extends EspressoDB's :code:`base.html` template.
Within this template, you can update the template blocks such that the default content gets replaced by the new block you provide.
For example, creating :code:`my_project/hamiltonian/templates/base.html` with the following code changes the existing app links to a single item of name `Link Name`.

.. code-block:: html

    {% extends 'base.html' %}

    {% block nav-app-links %}
    <li class="nav-item">
        <a class="nav-link" href="{% url 'app:name' %}">Link Name</a>
    </li>
    {% endblock nav-app-links %}

The :code:`{% url 'app:name' %}` templatetag looks up the :code:`urls.py` for the specified app and returns the URL for the view with the implemented name.

.. Note::
    EspressoDB uses `Bootstrap 4 navigation components <https://getbootstrap.com/docs/4.0/components/navs/>`_ to prettify the HTML view.
