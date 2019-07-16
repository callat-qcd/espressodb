"""
"""
import logging

from django.test import TestCase

from lattedb.correlator.models import Meson2pt

from lattedb.gaugeconfig.models import Hisq as HisqGauge

from lattedb.propagator.models import Hisq as HisqProp
from lattedb.propagator.models import MobiusDWF as MobiusDWFProp

from lattedb.gaugesmear.models import Unsmeared
from lattedb.gaugesmear.models import WilsonFlow

from lattedb.hadron.models import Meson

from lattedb.hadronsmear.models import HadronSmear
from lattedb.hadronsmear.models import Gaussian
from lattedb.hadronsmear.models import Unsmeared

# Create your tests here.


LOGGER = logging.getLogger("base")


class Meson2ptTestCase(TestCase):

    parameters = {
        "gagugeconfig": {
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
        },
        "propagator": {
            "mval": 10,
            "origin_x": 1,
            "origin_y": 2,
            "origin_z": 3,
            "origin_t": 10,
            "l5": 1,
            "m5": 2,
            "alpha5": 5,
            "a5": 10,
            "b5": 2,
            "c5": 5,
        },
        "hadron": {
            "structure": r"$\gamma_5$",
            "parity": 1,
            "spin_x2": 1,
            "spin_z_x2": 2,
            "isospin_x2": 3,
            "isospin_z_x2": 10000,
            "strangeness": 1,
        },
        "hadronsmear": {"radius": 10, "step": 2},
        "gaugesmear": {"flowtime": 1.0, "flowstep": 100},
        "meson2pt": {"momentum": 100},
    }

    def test_get_or_create_from_parameters(self):
        """
        """
        parameters = {}
        for pars in self.parameters.values():
            parameters.update(pars)

        Meson2pt.get_or_create_from_parameters(
            parameters,
            tree={
                "propagator0": (
                    "Hisq",
                    {"gaugeconfig": "Hisq", "gaugesmear": "Unsmeared"},
                ),
                "propagator1": (
                    "MobiusDWF",
                    {"gaugeconfig": "Hisq", "gaugesmear": "WilsonFlow"},
                ),
                "source": ("Meson", {"hadronsmear": "Gaussian"}),
                "sink": ("Meson", {"hadronsmear": "Unsmeared"}),
            },
        )

        hadron_smears = HadronSmear.objects.all()
        for hadron_smear, cls in zip(hadron_smears, [Gaussian, Unsmeared]):
            self.assertIsInstance(hadron_smear.specialization, cls)
            for key, val in parameters.items():
                if key in cls.__dict__:
                    self.assertEqual(val, getattr(hadron_smear.specialization, key))

        mesons = Meson.objects.all()
        for meson, smearing in zip(mesons, hadron_smears):
            self.assertEqual(meson.hadronsmear, smearing)
            for key, val in parameters.items():
                if key in Meson.__dict__:
                    self.assertEqual(val, getattr(meson, key))

        meson2pts = Meson2pt.objects.all()
        self.assertEqual(len(meson2pts), 1)
        meson2pt = meson2pts[0]
        for key, val in parameters.items():
            if key in meson2pt.__dict__:
                self.assertEqual(val, getattr(meson2pt, key))

        self.assertEqual(HisqProp.objects.count(), 1)
        self.assertEqual(MobiusDWFProp.objects.count(), 1)

        self.assertEqual(meson2pt.propagator0.specialization, HisqProp.objects.first())
        self.assertEqual(
            meson2pt.propagator1.specialization, MobiusDWFProp.objects.first()
        )
        self.assertEqual(meson2pt.source.specialization, mesons[0])
        self.assertEqual(meson2pt.sink.specialization, mesons[1])
