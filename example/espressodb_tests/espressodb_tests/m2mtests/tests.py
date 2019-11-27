# pylint: disable=C0103
"""Tests for models specific for the many to many signal logic app
"""
from unittest.mock import Mock
from unittest.mock import call

from django.test import TestCase

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

    def assertCallsEqual(self, calls_expected, calls_actual):
        """Asserts both calls are equal.

        Call structure is expecting args = QuerySet and arbitray kwargs.
        """
        self.assertEqual(len(calls_expected), len(calls_actual))

        for ce, ca in zip(calls_expected, calls_actual):
            _, arge, kwargse = ce
            _, arga, kwargsa = ca

            self.assertEqual(len(arge), 1)
            self.assertEqual(len(arga), 1)

            self.assertEqual(kwargsa, kwargse)

            qe = arge[0]
            qa = arge[0]

            self.assertQuerysetEqual(qe, qa, transform=lambda x: x, ordered=False)

    def test_01_single_m2m_single_instance(self):
        """Adds one m2m instance to set without reverse relation
        """
        B.check_m2m_consistency = Mock()

        self.b1.a_set.add(self.a1)
        self.assertEqual(self.b1.a_set.count(), 1)

        calls = [call(A.objects.filter(pk=self.a1.pk), column="a_set")]
        self.assertCallsEqual(
            calls_expected=calls, calls_actual=self.b1.check_m2m_consistency.mock_calls
        )

    def test_02_single_m2m_single_instance_reverse(self):
        """Adds one m2m instance to set with reverse relation
        """
        B.check_m2m_consistency = Mock()

        self.a1.b_set.add(self.b1)
        self.assertEqual(self.a1.b_set.count(), 1)

        calls = [call(A.objects.filter(pk=self.a1.pk), column="a_set")]
        self.assertCallsEqual(
            calls_expected=calls, calls_actual=self.b1.check_m2m_consistency.mock_calls
        )

    def test_03_single_m2m_multiple_instances(self):
        """Adds multiple m2m instance to set without reverse relation
        """
        B.check_m2m_consistency = Mock()

        self.b1.a_set.add(self.a1, self.a2)
        self.assertEqual(self.b1.a_set.count(), 2)

        calls = [call(A.objects.all(), column="a_set")]
        self.assertCallsEqual(
            calls_expected=calls, calls_actual=self.b1.check_m2m_consistency.mock_calls
        )

    def test_04_single_m2m_multiple_instances_reverse(self):
        """Adds multiple m2m instance to set with reverse relation
        """
        B.check_m2m_consistency = Mock()

        self.a1.b_set.add(self.b1, self.b2)
        self.assertEqual(self.a1.b_set.count(), 2)

        calls = [
            call(A.objects.filter(pk=self.a1.pk), column="a_set"),
            call(A.objects.filter(pk=self.a1.pk), column="a_set"),
        ]
        self.assertCallsEqual(
            calls_expected=calls, calls_actual=self.b1.check_m2m_consistency.mock_calls
        )
