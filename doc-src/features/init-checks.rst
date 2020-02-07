Automated cross-checks
----------------------

In a production environment, it is important to ensure that each Python connection to the database has the same definition of tables as the database itself.
This consistency can be ensured by automated checks which are run on the import of any EspressoDB project.
To turn on these checks, you have to set the environment variable

.. code::

    export ESPRESSODB_INIT_CHECKS=1

If set, the following checks are executed:

1. Check if all model fields are reflected in the migration files
2. Check if local migration files agree with the (remote) database

If any of the checks fail, EspressoDB will quit.

.. warning::
    The automated cross-checks were introduced in EspressoDB version 1.1.0.
    If you have created a project with prior versions of EspressoDB, you have to update the ``project/__init__.py`` ``_init()`` function as specified in :ref:`updating default behavior`.

.. note::
    Checks are only run when importing an EspressoDB project.
    The ``python manage.py`` command ignores cross-checks to allow applying migrations.




.. _updating default behavior:

Updating default behavior
=========================

The check function :func:`espressodb.management.checks.run_all_checks` is called in the ``_init()`` function of each  ``project/__init__.py``. For example, the ``my_project/__init__.py`` file of the `featured project <https://github.com/callat-qcd/espressodb/blob/master/example/my_project/my_project/__init__.py>`_ runs checks as follows

.. code::

    def _init():
        """Initializes the django environment for my_project
        """
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_project.config.settings")
        _setup()

        if os.environ.get("ESPRESSODB_INIT_CHECKS", "0") == "1":
            from espressodb.management.checks import run_all_checks

            try:
                run_all_checks()
            except Exception as error:
                msg = "Failed to import EspressoDB project!\n\n"
                msg += str(error)
                msg += "\n\nYou are seeing this error because,"
                msg += " on initialization, EspressoDB runs cross-checks."
                msg += " If you want to disable this behavior, set the"
                msg += " environment variable `ESPRESSODB_INIT_CHECKS=0`."

                raise RuntimeError(msg)

This function is run whenever you import your project.

EspressoDB projects before version 1.1.0 do not contain the above ``if`` statement.
Copy these lines in your project's ``_init()`` function to allow automated checks.

This ``_init()`` function is the place where you can globally change the default behavior for checks.
For example, to turn on checks if the ``ESPRESSODB_INIT_CHECKS`` is not set, change the ``if`` condition to

.. code ::

    if os.environ.get("ESPRESSODB_INIT_CHECKS", "1") != "0":
        ...
