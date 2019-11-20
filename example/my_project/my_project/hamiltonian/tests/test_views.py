"""Tests for views specific for the Hamiltonians app
"""
from django.test import TestCase

from bs4 import BeautifulSoup

from espressodb.base.utilities.apps import get_project_apps

from my_project.hamiltonian import models


class StatusViewTest(TestCase):
    """Tests for the status view of the example project
    """

    def test_status_page(self):
        """Tests the HTTP status of the client
        """
        response = self.client.get("/hamiltonian/status/")
        self.assertEqual(response.status_code, 200)


class DocumentationViewTest(TestCase):
    """Tests the documentation view
    """

    app_name = "my_project.hamiltonian"

    @property
    def content(self) -> BeautifulSoup:
        """Extracts the content of the view
        """
        response = self.client.get("/documentation/hamiltonian/")
        return BeautifulSoup(response.content, "html.parser")

    def test_01_page_status(self):
        """Tests the HTTP status of the client
        """
        response = self.client.get("/documentation/hamiltonian/")
        self.assertEqual(response.status_code, 200)

    def test_02_header(self):
        """Tests if the header of the doc page has the module name in doc string in it.
        """
        header = self.content.find("div", attrs={"class": "jumbotron"})
        self.assertIsNotNone(header)
        text = header.text
        self.assertIn(self.app_name, text)
        self.assertIn(models.__doc__, text)

    def test_03_models(self):
        """Tests if all model docs are rendered properly
        """
        app = [app for app in get_project_apps() if app.name == self.app_name][0]
        cards = self.content.find_all("div", attrs={"class": "card"})
        self.assertEqual(len(cards), len(app.models))

        for card in cards:
            self.assertIn(card.attrs.get("id"), app.models)
            model = app.models.get(card.attrs["id"])
            fields = set(tr.find("td").text for tr in card.find("tbody").find_all("tr"))
            expected_fields = {field.name for field in model.get_open_fields()}
            self.assertEqual(fields, expected_fields)
