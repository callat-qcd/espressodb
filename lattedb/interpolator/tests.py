"""Tests test_get_or_create_from_paramerters method
"""

from django.test import TestCase

from lattedb.base.tests import BaseTest

from lattedb.interpolator.models import Hadron

import lattedb.interpolatorsmear.tests as interpolatorsmear_tests


class InterpolatorTestCase(TestCase, BaseTest):

    cls = Hadron
    parameters = {
        "description": "Sad",
        "strangeness": 0.2,
        "irrep": "A1g",
        "embedding": 1,
        "parity": 0,
        "spin_x2": 1,
        "spin_z_x2": 2,
        "isospin_x2": 3,
        "isospin_z_x2": 10000,
        "momentum": 0,
    }
    test_tree = {"interpolatorsmear": interpolatorsmear_tests.InterpolatorSmearTestCase}
