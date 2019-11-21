"""Test case for notifications app
"""
from django.test import TestCase

from bs4 import BeautifulSoup

from django.contrib.auth.models import User

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
