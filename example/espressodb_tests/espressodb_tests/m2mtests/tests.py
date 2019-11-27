# pylint: disable=C0103
"""Tests for models specific for the many to many signal logic app
"""
from mock import patch

from django.test import TestCase

from espressodb.base.exceptions import ConsistencyError
from espressodb_tests.m2mtests.models import A, B, C


class M2MTest(TestCase):
    """Tests specific for the Eigenvalue model
    """

    def setUp(self):
        """Creates instances of test objects.
        """
        self.a1 = A.objects.create()
        self.a2 = A.objects.create()
        self.b1 = B.objects.create()
        self.b2 = B.objects.create()
        self.c1 = C.objects.create()
        self.c2 = C.objects.create()

    def test_01_single_m2m_single_instance(self):
        """Adds m2m one m2m instance to set without reverse relation
        """
        self.b1.a_set.add(self.a1)
