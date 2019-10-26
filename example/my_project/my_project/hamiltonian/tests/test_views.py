"""Tests for views specific for the Hamiltonians app
"""
from django.test import TestCase


class StatusViewTest(TestCase):
    """Tests for the status view of the example project
    """

    def test_status_page(self):
        """Tests the HTTP status of the client
        """
        response = self.client.get("/hamiltonian/status/")
        self.assertEqual(response.status_code, 200)
