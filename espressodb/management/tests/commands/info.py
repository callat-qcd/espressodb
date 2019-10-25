"""Tests for the info command
"""
import subprocess
import re
import os

from django.test import TestCase
from django.conf import settings


class InfoCommandTest(TestCase):
    """Test case for the ``espressodb info`` command
    """

    def test_command(self):
        """Runs the command and checks output
        """

        manage_py = os.path.join(settings.ROOT_DIR, "manage.py")
        self.assertTrue(os.path.exists(manage_py))

        out = (
            subprocess.check_output(["python", manage_py, "info"])
            .decode("utf-8")
            .split("\n")
        )
        pattern = r"espressodb version:"
        pattern += r" (?P<version>[0-9a-z]+)"
        pattern += r"(?: \((?P<branch>[0-9a-zA-Z\_\-\.]+)\))?"
        match = re.match(pattern, out[0])
        self.assertTrue(match)
