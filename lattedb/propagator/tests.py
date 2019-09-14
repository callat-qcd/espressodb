"""Tests test_get_or_create_from_paramerters method
"""

from django.test import TestCase

from lattedb.base.tests import BaseTest

from lattedb.propagator.models import OneToAll

import lattedb.gaugeconfig.tests as gaugeconfig_tests
import lattedb.fermionaction.tests as fermionaction_tests
import lattedb.quarksmear.tests as quarksmear_tests
import lattedb.wavefunction.tests as wavefunction_tests


class PropagatorTestCase(TestCase, BaseTest):

    cls = OneToAll
    parameters = {"origin_x": 1, "origin_y": 2, "origin_z": 3, "origin_t": 10}
    test_tree = {
        "fermionaction": fermionaction_tests.FermionActionTestCase,
        "gaugeconfig": gaugeconfig_tests.GaugeConfigTestCase,
        "sourcesmear": quarksmear_tests.QuarkSmearTestCase,
        "sinksmear": quarksmear_tests.QuarkSmearTestCase,
    }
