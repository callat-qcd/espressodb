"""Test case for notifications app
"""
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from bs4 import BeautifulSoup

from espressodb.notifications import get_notifier


class NotificationTestCase(TestCase):
    """Test case for notifications
    """

    def setUp(self):
        """Greps the notifier
        """
        self.username = "test user"
        self.password = "admin1234"

        user = User.objects.create(username=self.username)
        user.set_password(self.password)
        user.save()

        self.admin = "admin"
        self.admin_pw = "guest5678"

        admin = User.objects.create(username=self.admin)
        admin.set_password(self.admin_pw)
        admin.save()

        self.group = Group.objects.create(name="secret")
        self.group.user_set.add(admin)
        self.group.save()

        self.notifier = get_notifier()

    def test_global_message(self):
        """Sends an info message for all to see and checks if it appears on the homepage.
        """
        message = "This is a test"
        title = "Test"
        self.notifier.info(message, title=title)

        login = self.client.login(username=self.username, password=self.password)
        self.assertTrue(login)

        response = self.client.get("/notifications/")
        soup = BeautifulSoup(response.content, "html.parser")

        alert = soup.find("div", attrs={"class": "alert"})
        self.assertIsNotNone(alert)

        header = alert.find("h5").text
        self.assertEqual(header, title)

        content = alert.find("p").text
        self.assertEqual(message, content)

    def test_admin_as_user_message(self):
        """Sends an info message for admin to see and checks if it appears not on the
        homepage for regular user.
        """
        message = "This is an important message"
        title = "Secret"
        self.notifier.warning(message, title=title, groups=[self.group])

        login = self.client.login(username=self.username, password=self.password)
        self.assertTrue(login)

        response = self.client.get("/notifications/")
        soup = BeautifulSoup(response.content, "html.parser")

        alert = soup.find("div", attrs={"class": "alert"})
        self.assertIsNone(alert)

    def test_admin_as_admin_message(self):
        """Sends an info message for admin to see and checks if it appears on the
        homepage for admin user.
        """
        message = "This is an important message"
        title = "Secret"
        self.notifier.warning(message, title=title, groups=[self.group])

        login = self.client.login(username=self.admin, password=self.admin_pw)
        self.assertTrue(login)

        response = self.client.get("/notifications/")
        soup = BeautifulSoup(response.content, "html.parser")

        alert = soup.find("div", attrs={"class": "alert"})
        self.assertIsNotNone(alert)

        header = alert.find("h5").text
        self.assertEqual(header, title)

        content = alert.find("p").text
        self.assertEqual(message, content)
