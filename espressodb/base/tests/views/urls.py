"""Unittest for all present urls
"""
from django.test import TestCase

from django.contrib.auth.models import User

from espressodb.base.utilities.apps import get_apps_slug_map
import espressodb.base.utilities.blackmagicsorcery as re

URLS = ["/", "/populate/", "/populate-result/"]

LOGGED_IN_URLS = [
    "/notifications/",
    "/notifications/debug/",
    "/notifications/info/",
    "/notifications/warning/",
    "/notifications/error/",
    "/admin/",
    "/admin/auth/group/",
    "/admin/auth/user/",
    "/admin/notifications/notification/",
]


class URLViewTest(TestCase):
    """Tests if all urls are present
    """

    exclude_urls = []

    @classmethod
    def url_excluded(cls, url: str) -> bool:
        """Checks if the url is in the exclude_urls pattern list

        Arguments:
            url: Regex pattern to match.
        """
        return any([re.match(pattern, url) is not None for pattern in cls.exclude_urls])

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
            if self.url_excluded(url):
                continue

            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_logged_in_urls_as_logged_out(self):
        """Tests wether login required URLS are present but require login.
        """
        for url in LOGGED_IN_URLS:
            if self.url_excluded(url):
                continue

            with self.subTest(url=url):
                with self.subTest(follow=False):
                    response = self.client.get(url, follow=False)
                    self.assertEqual(response.status_code, 302)

                with self.subTest(follow=True):
                    response = self.client.get(url, follow=True)
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(
                        response.redirect_chain[-1][0],
                        ("/admin" if "admin" in url else "") + f"/login/?next={url}",
                    )

    def test_logged_in_urls_as_logged_in(self):
        """Tests wether login required URLS are present and viewable by logged in user.
        """
        login = self.client.login(username=self.username, password=self.password)
        self.assertTrue(login)

        for url in LOGGED_IN_URLS:
            if self.url_excluded(url):
                continue

            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302 if "admin" in url else 200)

    def test_documentation_pages(self):
        """Tests wether documentation pages are present for each project app with models.
        """
        for app_slug, app in get_apps_slug_map().items():

            if not app.get_models():
                continue

            url = f"/documentation/{app_slug}/"
            with self.subTest(app=app, url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
