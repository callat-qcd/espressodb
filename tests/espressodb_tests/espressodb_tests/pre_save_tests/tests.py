# pylint: disable=C0103
"""Tests for models specific for the many to many signal logic app
"""
from logging import getLogger

from unittest.mock import patch

from django.test import TestCase

from espressodb.base.exceptions import ConsistencyError

from espressodb_tests.pre_save_tests.models import MandatoryTagTable
from espressodb_tests.pre_save_tests.models import OptionalTagTable
from espressodb_tests.pre_save_tests.models import VERSION


LOGGER = getLogger("espressodb")


class PreSafeTest(TestCase):  # pylint: disable=R0902
    """Tests pre_save execution
    """

    @patch.object(MandatoryTagTable, "pre_save")
    def test_01_pre_save_mandatory_called(self, mock):
        """Tests if pre_save is called for mandatory table
        """
        with self.assertRaises(ConsistencyError):
            MandatoryTagTable.objects.create()

        self.assertTrue(mock.called)

    def test_02_pre_save_mandatory_write(self):
        """Tests if pre_save is desired outcome for mandatory table
        """
        MandatoryTagTable.objects.create()

        objects = MandatoryTagTable.objects.all()
        self.assertEqual(objects.count(), 1)

        instance = objects.first()
        self.assertEqual(instance.tag, VERSION)

    @patch.object(OptionalTagTable, "pre_save")
    def test_03_pre_save_optional_not_called(self, mock):
        """Tests if pre_save is called not called for optional table when disabled
        """
        OptionalTagTable.run_pre_save = False

        OptionalTagTable.objects.create()
        self.assertFalse(mock.called)

    @patch.object(MandatoryTagTable, "pre_save")
    def test_04_pre_save_mandatory_not_called_faills(self, mock):
        """Tests if pre_save is called not called for optional table when disabled
        """
        MandatoryTagTable.run_pre_save = False

        with self.assertRaises(ConsistencyError):
            MandatoryTagTable.objects.create()

        self.assertFalse(mock.called)
