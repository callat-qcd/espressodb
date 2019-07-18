"""Tests test_get_or_create_from_paramerters method
"""

from django.test import TestCase


from lattedb.ensemble.models import Ensemble
from lattedb.ensemble.models import Flavor211

# Create your tests here.


class HisqTestCase(TestCase):

    creation_parameters = {
        "short_tag": "a15m310",
        "stream": "a",
        "nconfig": 500,
        "nx": 48,
        "nt": 64,
        "ml": 1.0,
        "ms": 2.0,
        "mc": 3.0,
        "beta": 4.0,
        "naik": 5.0,
        "u0": 6.0,
        "a_fm": 7.0,
        "l_fm": 8.0,
        "mpil": 16.0,
        "mpi": 2.0,
    }

    def test_get_or_create(self):
        """
        """
        hisq, created = Flavor211.objects.get_or_create(**self.creation_parameters)
        self.assertTrue(created)

        for key, val in self.creation_parameters.items():
            with self.subTest(column=key):
                self.assertEqual(val, getattr(hisq, key))

    def test_get_or_create_from_parameters(self):
        """
        """
        instance, instances = Flavor211.get_or_create_from_parameters(
            self.creation_parameters
        )

        self.assertEqual(len(instances), 1)

        instance, created = instances[0]
        self.assertTrue(created)

        for key, val in self.creation_parameters.items():
            with self.subTest(column=key):
                self.assertEqual(val, getattr(instance, key))
