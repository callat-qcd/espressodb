# pylint: disable=C0103
"""Tests of customizations of EspressoDB
"""
from logging import getLogger

from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase

from bs4 import BeautifulSoup

from espressodb_tests.customizations.models import CB

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


class BaseStringTest(TestCase):
    """
    """

    def test_01_default_str(self):
        """Test EspressoDB string

        The class `CB` does not implement a default string.
        Thus one would expect the default espressodb behavior.
        """

        # Test string for value which does not default to False
        b = CB(value=1).save()
        self.assertEqual(str(b), f"CB[Base](value={b.value})")

        # Test string for value which defaults to False
        b = CB(value=0).save()
        self.assertEqual(str(b), f"CB[Base](value={b.value})")

        # Test string for value which defaults to None
        b = CB(value=None).save()
        self.assertEqual(str(b), f"CB[Base]")

    def test_02_str_overload(self):
        """Test EspressoDB string

        The class `CB` does not implement a default string.
        Thus one would expect the default espressodb behavior.
        """
        new_str = lambda obj: f"CB->value: {obj.value}"

        with patch.object(CB, "__str__", new=new_str):
            b = CB(value=1).save()
            self.assertEqual(str(b), new_str(b))


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
