"""Tests for the index page
"""
from django.test import TestCase


class IndexViewTest(TestCase):
    """Tests for the index view of the example project
    """

    def test_index_page(self):
        """Tests the HTTP status of the client
        """
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
