"""
"""
import logging

from django.test import TestCase
from django.db import connection
from django.apps import apps

from django.conf import settings


# Create your tests here.

LOGGER = logging.getLogger("base")


class BaseTest:
    """Abstract implementation of a table class test
    """

    cls = None
    test_tree = None

    parameters = None
    test_tree = None

    @classmethod
    def check(cls, instance, parameters):
        # ToDo: check recursive columns using subtests
        for key in cls.parameters:
            if key in cls.cls.__dict__:
                value = getattr(instance.specialization, key)
                field = [
                    field for field in cls.cls._meta.get_fields() if field.name == key
                ][0]
                if value != field.get_db_prep_value(parameters[key], connection):
                    raise ValueError(
                        "%s parameters for %s not agree with input:\n%s != %s"
                        % (instance, key, value, parameters[key])
                    )

    @classmethod
    def get_parameters(cls):
        pars = cls.parameters
        for sub_test in (cls.test_tree or {}).values():
            pars.update(sub_test.get_parameters())
        return pars

    @classmethod
    def get_tree(cls):
        tree = {}
        for key, sub_test in (cls.test_tree or {}).items():
            tree[key] = sub_test.cls.__name__

            sub_test_tree = sub_test.get_tree() or {}
            for sub_key, val in sub_test_tree.items():
                tree[f"{key}.{sub_key}"] = val

        return tree

    def test_get_or_create_from_parameters(self):
        """Tests get or create from parameters method

        Creates an instance and checks attributes.
        """
        parameters = self.get_parameters()
        tree = self.get_tree()
        LOGGER.debug("Working with the following tree:\n%s", tree)
        LOGGER.debug("Working with the following parameters:\n%s", parameters)

        self.cls.get_or_create_from_parameters(parameters, tree=tree)

        # Get created object
        instance = self.cls.objects.last()
        # check if parameters correct
        self.check(instance, parameters)


class AppTest(TestCase):
    """Tests if expected apps are present
    """

    def test_installed_apps(self):
        """Checks if apps found in project settings are actually installed
        """

        installed_apps = set(el.name for el in apps.app_configs.values())
        project_apps = set(settings.PROJECT_APPS)

        self.assertTrue(
            project_apps.issubset(installed_apps),
            msg="Found project apps which have not been installed:\n%s"
            % project_apps.difference(installed_apps),
        )
