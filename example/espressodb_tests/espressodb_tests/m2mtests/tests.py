# pylint: disable=C0103
"""Tests for models specific for the many to many signal logic app
"""
from logging import getLogger

from django.test import TestCase

from espressodb_tests.m2mtests.models import A, B, C


LOGGER = getLogger("espressodb")


def record_calls(calls):
    """Decorator with arguments to record calls of function (also saving the instance)
    """

    def decorator(function):
        "Wraps the function itself"

        def wrapper(*args, **kwargs):
            "Records the calls for the function"
            calls.append((args, kwargs))
            return function(*args, **kwargs)

        return wrapper

    return decorator


class M2MTest(TestCase):  # pylint: disable=R0902
    """Tests m2m check consistency calls
    """

    def setUp(self):
        """Creates instances of test objects.
        """
        self.b_calls = []
        self.c_calls = []

        B.check_m2m_consistency = record_calls(self.b_calls)(B.check_m2m_consistency)
        C.check_m2m_consistency = record_calls(self.c_calls)(C.check_m2m_consistency)

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

        counter = 0
        for ce, ca in zip(calls_expected, calls_actual):
            counter += 1
            arge, kwargse = ce
            arga, kwargsa = ca

            self.assertEqual(len(arge), 2)
            self.assertEqual(len(arga), 2)

            self.assertEqual(
                kwargsa,
                kwargse,
                msg=f"Kwargs of call {counter} not equal."
                f"\n\t{ce} != {ca}"
                f"\n\t{kwargse} != {kwargsa}",
            )

            inste = arge[0]
            insta = arga[0]

            self.assertEqual(
                insta,
                inste,
                msg=f"Instances of call {counter} not equal."
                f"\n\t{ce} != {ca}"
                f"\n\t{inste} != {insta}",
            )
            qe = arga[1]
            qa = arge[1]

            self.assertQuerysetEqual(
                qe,
                qa,
                transform=lambda x: x,
                ordered=False,
                msg=f"QuerySet of call {counter} not equal."
                f"\n\t{ce} != {ca}"
                f"\n\t{qe} != {qa}",
            )

    def test_01_single_m2m_single_instance(self):
        """Adds one m2m instance to set without reverse relation
        """
        self.b1.a_set.add(self.a1)

        self.assertEqual(self.b1.a_set.count(), 1)
        self.assertEqual(self.a1.b_set.count(), 1)

        calls = [((self.b1, A.objects.filter(pk=self.a1.pk)), {"column": "a_set"})]
        self.assertCallsEqual(calls, self.b_calls)

    def test_02_single_m2m_single_instance_reverse(self):
        """Adds one m2m instance to set with reverse relation
        """
        self.a1.b_set.add(self.b1)

        self.assertEqual(self.a1.b_set.count(), 1)
        self.assertEqual(self.b1.a_set.count(), 1)

        calls = [((self.b1, A.objects.filter(pk=self.a1.pk)), {"column": "a_set"})]
        self.assertCallsEqual(calls, self.b_calls)

    def test_03_single_m2m_multiple_instances(self):
        """Adds multiple m2m instance to set without reverse relation
        """
        self.b1.a_set.add(self.a1, self.a2)

        self.assertEqual(self.b1.a_set.count(), 2)
        self.assertEqual(self.a1.b_set.count(), 1)
        self.assertEqual(self.a2.b_set.count(), 1)

        calls = [((self.b1, A.objects.all()), {"column": "a_set"})]
        self.assertCallsEqual(calls, self.b_calls)

    def test_04_single_m2m_multiple_instances_reverse(self):
        """Adds multiple m2m instance to set with reverse relation
        """
        self.a1.b_set.add(self.b1, self.b2)

        self.assertEqual(self.a1.b_set.count(), 2)
        self.assertEqual(self.b1.a_set.count(), 1)
        self.assertEqual(self.b2.a_set.count(), 1)

        calls = [
            ((self.b1, A.objects.filter(pk=self.a1.pk)), {"column": "a_set"}),
            ((self.b2, A.objects.filter(pk=self.a1.pk)), {"column": "a_set"}),
        ]
        self.assertCallsEqual(calls, self.b_calls)

    def test_05_multicol_m2m_multiple_instances(self):
        """Adds multiple m2m instances to m2m wit two m2m columns without reverse
        """
        self.c1.b_set.add(self.b1, self.b2)
        self.c1.a_set.add(self.a2, self.a1)

        self.assertEqual(self.a1.c_set.count(), 1)
        self.assertEqual(self.a2.c_set.count(), 1)
        self.assertEqual(self.b1.c_set.count(), 1)
        self.assertEqual(self.b2.c_set.count(), 1)
        self.assertEqual(self.c1.a_set.count(), 2)
        self.assertEqual(self.c1.a_set.count(), 2)

        calls = [
            ((self.c1, B.objects.all()), {"column": "b_set"}),
            ((self.c1, A.objects.all()), {"column": "a_set"}),
        ]
        self.assertCallsEqual(calls, self.c_calls)

    def test_06_multicol_m2m_multiple_instances_reverse(self):
        """Adds multiple m2m instance to set with reverse relation
        """
        self.b1.c_set.add(self.c1, self.c2)
        self.a1.c_set.add(self.c2, self.c1)

        self.assertEqual(self.a1.c_set.count(), 2)
        self.assertEqual(self.b1.c_set.count(), 2)
        self.assertEqual(self.c1.a_set.count(), 1)
        self.assertEqual(self.c2.a_set.count(), 1)
        self.assertEqual(self.c1.b_set.count(), 1)
        self.assertEqual(self.c2.b_set.count(), 1)

        calls = [
            ((self.c1, B.objects.filter(pk=self.b1.pk)), {"column": "b_set"}),
            ((self.c2, B.objects.filter(pk=self.b1.pk)), {"column": "b_set"}),
            # Note that the order has changed!
            ((self.c1, A.objects.filter(pk=self.a1.pk)), {"column": "a_set"}),
            ((self.c2, A.objects.filter(pk=self.a1.pk)), {"column": "a_set"}),
        ]
        self.assertCallsEqual(calls, self.c_calls)
