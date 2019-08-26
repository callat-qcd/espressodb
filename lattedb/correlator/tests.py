"""Tests test_get_or_create_from_paramerters method
"""

from django.test import TestCase

from lattedb.base.tests import BaseTest

from lattedb.correlator.models import Meson2pt

import lattedb.propagator.tests as propagator_tests
import lattedb.interpolator.tests as interpolator_tests


class Meson2ptTestCase(TestCase, BaseTest):

    cls = Meson2pt
    parameters = {}  # {"source.description": "source"}
    test_tree = {
        "propagator0": propagator_tests.PropagatorTestCase,
        "propagator1": propagator_tests.PropagatorTestCase,
        "sink": interpolator_tests.InterpolatorTestCase,
        "source": interpolator_tests.InterpolatorTestCase,
    }
