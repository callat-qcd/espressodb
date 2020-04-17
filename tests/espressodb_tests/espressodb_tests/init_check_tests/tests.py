"""Checks if the run_all_checks method is called depending on state of the
ESPRESSODB_INIT_CHECKS environment variable.
"""
import os
from unittest.mock import patch
import importlib

from django.test import TestCase

from espressodb.management import checks

import espressodb_tests

# Create your tests here.


class RunCheckTest(TestCase):
    """Checks if the run_all_checks method is called depending on state of the
    ESPRESSODB_INIT_CHECKS environment variable.
    """

    @patch.object(checks, "run_all_checks")
    def test_01_checks_run_with_unset_flag(self, mock):
        """Sets the ESPRESSODB_INIT_CHECKS environment variable to zero to check if
        run_all_checks is called.
        """
        os.environ.pop("ESPRESSODB_INIT_CHECKS", None)

        importlib.reload(espressodb_tests)

        self.assertFalse(mock.called)

    @patch.object(checks, "run_all_checks")
    def test_02_checks_run_with_set_zero_flag(self, mock):
        """Sets the ESPRESSODB_INIT_CHECKS environment variable to zero to check if
        run_all_checks is not called.
        """
        os.environ["ESPRESSODB_INIT_CHECKS"] = "0"

        importlib.reload(espressodb_tests)

        self.assertFalse(mock.called)

    @patch.object(checks, "run_all_checks")
    def test_03_checks_run_with_set_flag(self, mock):
        """Sets the ESPRESSODB_INIT_CHECKS environment variable to zero to check if
        run_all_checks is called.
        """
        os.environ["ESPRESSODB_INIT_CHECKS"] = "1"

        importlib.reload(espressodb_tests)

        self.assertTrue(mock.called)
