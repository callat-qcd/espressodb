# pylint: disable=C0103
"""Tests of customizations of EspressoDB
"""
from logging import getLogger

from django.contrib.auth.models import User
from django.test import TestCase

from bs4 import BeautifulSoup


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


class NavbarLinkTest(TestCase):
    """Checks for extending the navbar template
    """

    def test_01_template_used(self):
        """Checks if correct template is used
        """
        url = ""
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateNotUsed(response, "customized-index.html")
        self.assertTemplateUsed(response, "index.html")

        url = "/customizations/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "customized-index.html")
        self.assertTemplateNotUsed(response, "index.html")

    def test_02_navbar_items(self):
        """Checks if the customized navbar only shows the Index link
        """
        url = "/customizations/"
        response = self.client.get(url)

        soup = BeautifulSoup(response.content)
        customized_links = [
            a.text
            for a in soup.find("ul").find_all("a")
            if not "dropdown-toggle" in a.attrs.get("class", [])
        ]

        self.assertEqual(len(customized_links), 1)
        self.assertEqual(customized_links[0], "Index")
