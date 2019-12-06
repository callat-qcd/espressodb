"""Tests for the index page
"""
from typing import Set

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import get_resolver
from django.urls import resolve, Resolver404

from bs4 import BeautifulSoup

from espressodb.base.utilities.apps import get_apps_slug_map
import espressodb.base.utilities.blackmagicsorcery as re


class IndexViewTest(TestCase):
    """Tests for the index view of the example project
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
        self.user = User.objects.create(username=self.username)
        self.user.set_password(self.password)
        self.user.save()

    def test_index_page(self):
        """Tests the HTTP status of the client
        """
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    @staticmethod
    def get_links(response) -> Set[str]:
        """Finds all the links present in the navbar (which ar not ["/", "#"]).
        """
        soup = BeautifulSoup(response.content, "html.parser")
        nav = soup.find("nav")
        return set(
            link["href"]
            for link in nav.findAll("a", href=True)
            if link["href"] not in ["/", "#"]
        )

    def test_link_list_as_logged_out(self):
        """Tests wether all links in the link list are present
        """
        expected_links = {"/populate/", "/login/"}

        for app_slug, app in get_apps_slug_map().items():
            for patterns in get_resolver(app.name + ".urls").reverse_dict.values():
                url = f"/{app_slug}/{patterns[0][0][0]}"
                try:
                    resolve(url)
                    if not self.url_excluded(url):
                        expected_links.add(url)
                except Resolver404:
                    pass

            if app.get_models():
                expected_links.add(f"/documentation/{app_slug}/")

        response = self.client.get("/")
        self.assertTrue("index.html" in response.template_name)
        self.assertEqual(expected_links, self.get_links(response))

    def test_link_list_as_logged_in(self):
        """Tests wether all links in the link list are present as logged in user
        """
        self.client.login(username=self.username, password=self.password)
        expected_links = {"/populate/", "/logout/", "/notifications/"}
        for level in ["debug", "info", "warning", "error"]:
            expected_links.add(f"/notifications/{level}/")

        for app_slug, app in get_apps_slug_map().items():
            for patterns in get_resolver(app.name + ".urls").reverse_dict.values():
                url = f"/{app_slug}/{patterns[0][0][0]}"
                if not self.url_excluded(url):
                    expected_links.add(url)

            if app.get_models():
                expected_links.add(f"/documentation/{app_slug}/")

        response = self.client.get("/")
        self.assertTrue("index.html" in response.template_name)
        self.assertEqual(expected_links, self.get_links(response))

    def test_link_list_as_staff(self):
        """Tests wether all links in the link list are present as staff user
        """
        self.user.is_staff = True
        self.user.save()
        self.client.login(username=self.username, password=self.password)
        expected_links = {"/populate/", "/logout/", "/admin/", "/notifications/"}
        for level in ["debug", "info", "warning", "error"]:
            expected_links.add(f"/notifications/{level}/")

        for app_slug, app in get_apps_slug_map().items():
            for patterns in get_resolver(app.name + ".urls").reverse_dict.values():
                url = f"/{app_slug}/{patterns[0][0][0]}"
                if not self.url_excluded(url):
                    expected_links.add(url)

            if app.get_models():
                expected_links.add(f"/documentation/{app_slug}/")

        response = self.client.get("/")
        self.assertTrue("index.html" in response.template_name)
        self.assertEqual(expected_links, self.get_links(response))
