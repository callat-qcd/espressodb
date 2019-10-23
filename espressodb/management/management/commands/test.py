"""Interface to Django's test command
"""
import logging

from django.core.management.commands.test import Command as TestCommand

LOGGER = logging.getLogger("espressodb")


class Command(TestCommand):
    """Command for running unittests of espressodb and the example project.
    """

    help = "Discover and run tests in the specified modules or the current directory."

    def handle(self, *test_labels, **options):
        """Overrides Django's default test command by overriding the `test_labes`.
        """
        test_labels = ("espressodb", "my_project")
        super().handle(*test_labels, **options)
