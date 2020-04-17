# pylint: disable=C0103
"""Tests of customizations of EspressoDB
"""
from logging import getLogger

from django.contrib.auth.models import User
from django.test import TestCase


LOGGER = getLogger("espressodb")


class AminPageTest(TestCase):
    """Checks for customizations of the admin page
    """

    def setUp(self):
        """Create a user for the test
        """
        self.username = "test user"
        self.password = "admin1234"
        user = User.objects.create(username=self.username)
        user.is_staff = True
        user.is_superuser = True
        user.set_password(self.password)
        user.save()

    def test_model_excluded_from_admin(self):
        """The admin.py file of this module excludes the CA model. This test checks if
        only the CB model is found on the admin page.
        """
        login = self.client.login(username=self.username, password=self.password)
        self.assertTrue(login)

        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 200)

        app_context_data = [
            app
            for app in response.context_data["available_apps"]
            if app["app_label"] == "customizations"
        ]
        self.assertEqual(len(app_context_data), 1)

        admin_models = app_context_data[0]["models"]
        self.assertEqual(len(admin_models), 1)
        self.assertEqual(admin_models[0]["object_name"], "CB")
