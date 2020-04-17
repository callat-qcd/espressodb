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
