"""Tests for views specific for the Hamiltonians app
"""
from django.test import TestCase

from bs4 import BeautifulSoup

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

    @property
    def content(self) -> BeautifulSoup:
        """Extracts the content of the view
        """
        response = self.client.get("/documentation/hamiltonian/")
        return BeautifulSoup(response.content, "html.parser")

    def test_status_page(self):
        """Tests the HTTP status of the client
        """
        response = self.client.get("/documentation/hamiltonian/")
        self.assertEqual(response.status_code, 200)

    def test_header(self):
        """Tests if the header of the doc page has the module name in doc string in it.
        """
        header = self.content.find("div", attrs={"class": "jumbotron"})
        self.assertIsNotNone(header)
        text = header.text
        self.assertIn("my_project.hamiltonian", text)
        self.assertIn(models.__doc__, text)

    def test_models(self):
        """
        """
