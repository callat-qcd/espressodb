"""Tests for management
"""
import logging

from django.test import TestCase
from django.apps import apps

from django.conf import settings


LOGGER = logging.getLogger("espressodb")


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
