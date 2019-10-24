"""Unittest for all present urls
"""
from django.test import TestCase

from django.contrib.auth.models import User

URLS = ["/", "/populate/", "/populate-result/"]

LOGGED_IN_URLS = [
    "/notifications/",
    "/notifications/debug/",
    "/notifications/info/",
    "/notifications/warning/",
    "/notifications/error/",
]

APP_DEPNEND_URLS = ["documentation/{app_slug}"]


class URLViewTest(TestCase):
    """Tests if all urls are present
    """

    def setUp(self):
        """Create a user for the test
        """
        self.username = "test user"
        self.password = "admin1234"
        user = User.objects.create(username=self.username)
        user.set_password(self.password)
        user.save()

    def test_open_urls(self):
        """Tests the HTTP status of the client.
        """
        for url in URLS:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_logged_in_urls_as_logged_out(self):
        """Tests wether login required URLS are present but require login.
        """
        for url in LOGGED_IN_URLS:
            with self.subTest(url=url):
                with self.subTest(follow=False):
                    response = self.client.get(url, follow=False)
                    self.assertEqual(response.status_code, 302)

                with self.subTest(follow=True):
                    response = self.client.get(url, follow=True)
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(
                        response.redirect_chain[-1][0], f"/login/?next={url}"
                    )

    def test_logged_in_urls_as_logged_in(self):
        """Tests wether login required URLS are present and viewable by logged in user.
        """
        login = self.client.login(username=self.username, password=self.password)
        self.assertTrue(login)

        for url in LOGGED_IN_URLS:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
