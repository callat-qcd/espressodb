"""Tests test_get_or_create_from_paramerters method
"""

from django.test import TestCase

from lattedb.base.tests import BaseTest

from lattedb.gaugeconfig.models import Nf211

import lattedb.gaugesmear.tests as gaugesmear_tests
import lattedb.gaugeaction.tests as gaugeaction_tests
import lattedb.fermionaction.tests as fermionaction_tests

# Create your tests here.


class GaugeConfigTestCase(TestCase, BaseTest):

    cls = Nf211
    parameters = {
        "short_tag": "a15m310",
        "stream": "a",
        "config": 500,
        "nx": 48,
        "ny": 48,
        "nz": 48,
        "nt": 64,
        "l_fm": 8.0,
        "models.CASCADE": 10.0,
        "mpi": 100.0,
        "light.quark_mass": 0.2,
        "light.quark_tag": "up",
        "strange.quark_mass": 0.4,
        "strange.quark_tag": "s",
        "charm.quark_mass": 0.6,
        "charm.quark_tag": "c",
    }
    test_tree = {
        "gaugeaction": gaugeaction_tests.GaugeActionTestCase,
        "gaugesmear": gaugesmear_tests.GaugeSmearTestCase,
        "light": fermionaction_tests.FermionActionTestCase,
        "strange": fermionaction_tests.FermionActionTestCase,
        "charm": fermionaction_tests.FermionActionTestCase,
    }
