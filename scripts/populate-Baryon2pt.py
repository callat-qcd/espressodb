#!/usr/bin/env python
# coding: utf-8
"""Scripts which populates the Baryon2pt functions with inital data
"""


from typing import Dict, Any

import os
import re
from itertools import product

from tqdm import tqdm

import logging

from lattedb.correlator.models import Baryon2pt


LOGGER = logging.getLogger("base")
LOGGER.setLevel(logging.INFO)


FDIR = os.path.dirname(os.path.realpath(__file__))
DATA = os.path.abspath(os.path.join(FDIR, os.pardir, "notebooks", "data"))

files = os.listdir(DATA)

text = ""

for file in files:
    with open(os.path.join(DATA, file), "r") as inp:
        text += inp.read()

data = [key for key in text.split("\n") if key.endswith(".lime")]


def parse_ensemble(short_tag: str) -> Dict[str, Any]:

    long_tag = {
        "a15m310L": "l2448f211b580m013m065m838",
        "a12m310": "l2464f211b600m0102m0509m635",
        "a09m310": "l3296f211b630m0074m037m440",
    }
    key = long_tag[short_tag]

    pattern = (
        "l"
        "(?P<nx>[0-9]{2})"
        "(?P<nt>[0-9]{2})"
        "f211"
        "b(?P<beta>[0-9]{3})"
        "m(?P<light__quark_mass>[0-9]+)"
        "m(?P<strange__quark_mass>[0-9]+)"
        "m(?P<charm__quark_mass>[0-9]+)"
    )
    type_map = {
        "nx": str,
        "nt": str,
        "beta": lambda beta: ".".join([beta[:-2], beta[-2:]]),
        "light__quark_mass": lambda mass: f"0.{mass}",
        "strange__quark_mass": lambda mass: f"0.{mass}",
        "charm__quark_mass": lambda mass: f"0.{mass}",
    }

    match = re.match(pattern, key)

    info = (
        {
            key: type_map[key](val)
            for key, val in match.groupdict().items()
            if key in type_map
        }
        if match
        else {}
    )
    info["ny"] = info["nz"] = info["nx"]

    ## from https://arxiv.org/pdf/1212.4768.pdf TAB IV

    charm_naik = {"5.80": "-0.3582", "6.00": "-0.2308", "6.30": "-0.1204"}
    info["light__naik"] = "0.0"
    info["strange__naik"] = "0.0"
    info["charm__naik"] = charm_naik[info["beta"]]

    u0 = {"5.80": "0.8553", "6.00": "0.86372", "6.30": "0.874164"}
    info["u0"] = u0[info["beta"]]

    return info


def parse_propagator(key) -> Dict[str, Any]:
    pattern = (
        "(?P<config>[0-9]+)"
        "/"
        "prop_"
        "(?P<short_tag>a[0-9]+m[0-9]+L?)"
        "_"
        "(?P<stream>[a-z]{1})"
        "_[0-9]+_"
        "gf(?P<flowtime>[0-9\.]+)"
        "_"
        "w(?P<radius>[0-9\.]+)"
        "_"
        "n(?P<step>[0-9]+)"
        "_"
        "M5(?P<m5>[0-9\.]+)"
        "_"
        "L5(?P<l5>[0-9]+)"
        "_"
        "a(?P<alpha5>[0-9\.]+)"
        "_"
        "mq(?P<MobiusDWF__quark_mass>[0-9\.]+)"
        "_"
        "x(?P<origin_x>[0-9]+)"
        "y(?P<origin_y>[0-9]+)"
        "z(?P<origin_z>[0-9]+)"
        "t(?P<origin_t>[0-9]+)"
    )
    match = re.match(pattern, key)

    info = match.groupdict() if match else {}

    info["a_fm"] = info["short_tag"].replace("a", "0.").split("m")[0]
    info["mpi"] = info["short_tag"].replace("a", "0.").split("m")[1].replace("L", "")

    ## https://c51.lbl.gov/wiki/mdwf_hisq existing ensembles
    c5 = {"a09m310": "0.25", "a12m310": "0.25", "a15m310L": "0.5"}

    b5 = {"a09m310": "1.25", "a12m310": "1.25", "a15m310L": "1.5"}

    info["c5"] = c5[info["short_tag"]]
    info["b5"] = c5[info["short_tag"]]

    info.update(parse_ensemble(info["short_tag"]))

    return info


key = "300/prop_a09m310_e_300_gf1.0_w3.5_n45_M51.1_L56_a1.5_mq0.00951_x3y3z19t62.lime"


variable = None

global_pars = {
    # Additional Gauge Config Smearing
    "flowstep": 40,
    "flowtime": variable,
    # Gauge Config
    "config": variable,
    "nt": variable,
    "nx": variable,
    "ny": variable,
    "nz": variable,
    "mpi": 310,
    "short_tag": variable,
    "stream": variable,
    # Gauge action
    "beta": variable,
    "a_fm": variable,
    "u0": variable,
    # OneToAll
    "origin_x": variable,
    "origin_y": variable,
    "origin_z": variable,
    "origin_t": variable,
    # MobiusDW
    "b5": variable,
    "c5": variable,
    "l5": variable,
    "m5": variable,
    # Hisq
    "naik": variable,
    # Hadron Gaussian Smear
    "radius": variable,
    "step": variable,
    # Interpolator: Hadron
    "strangeness": 0,
    "description": "nucleon interpolation operator [hep-lat/0508018]",
    "irrep": "g1",
    "embedding": 1,
    "parity": variable,
    "spin_x2": 1,
    "spin_z_x2": variable,
    "isospin_x2": 1,
    "isospin_z_x2": variable,
    "momentum": 0,
}


special_pars = {
    ## Specializations ##
    # Valence
    # hack to resolve same instanziation fix
    "propagator0.fermionaction.quark_mass": variable,
    "propagator1.fermionaction.quark_mass": variable,
    "propagator2.fermionaction.quark_mass": variable,
    "propagator0.fermionaction.quark_tag": "light",
    "propagator1.fermionaction.quark_tag": "light",
    "propagator2.fermionaction.quark_tag": "light",
    # Sea
    "propagator0.gaugeconfig.light.quark_mass": variable,
    "propagator1.gaugeconfig.light.quark_mass": variable,
    "propagator2.gaugeconfig.light.quark_mass": variable,
    "propagator0.gaugeconfig.strange.quark_mass": variable,
    "propagator1.gaugeconfig.strange.quark_mass": variable,
    "propagator2.gaugeconfig.strange.quark_mass": variable,
    "propagator0.gaugeconfig.charm.quark_mass": variable,
    "propagator1.gaugeconfig.charm.quark_mass": variable,
    "propagator2.gaugeconfig.charm.quark_mass": variable,
    "propagator0.gaugeconfig.light.quark_tag": "light",
    "propagator1.gaugeconfig.light.quark_tag": "light",
    "propagator2.gaugeconfig.light.quark_tag": "light",
    "propagator0.gaugeconfig.strange.quark_tag": "strange",
    "propagator1.gaugeconfig.strange.quark_tag": "strange",
    "propagator2.gaugeconfig.strange.quark_tag": "strange",
    "propagator0.gaugeconfig.charm.quark_tag": "charm",
    "propagator1.gaugeconfig.charm.quark_tag": "charm",
    "propagator2.gaugeconfig.charm.quark_tag": "charm",
}


tree = {
    "propagator0": "OneToAll",
    "propagator0.fermionaction": "MobiusDW",
    "propagator0.fermionaction.linksmear": "WilsonFlow",
    "propagator0.gaugeconfig": "Nf211",
    "propagator0.gaugeconfig.light": "Hisq",
    "propagator0.gaugeconfig.light.linksmear": "WilsonFlow",
    "propagator0.gaugeconfig.strange": "Hisq",
    "propagator0.gaugeconfig.strange.linksmear": "WilsonFlow",
    "propagator0.gaugeconfig.charm": "Hisq",
    "propagator0.gaugeconfig.charm.linksmear": "WilsonFlow",
    "propagator0.gaugeconfig.gaugeaction": "LuescherWeisz",
    "propagator0.sourcesmear": "GaugeCovariantGaussian",
    "propagator0.sinksmear": "Point",
    # p1
    "propagator1": "OneToAll",
    "propagator1.fermionaction": "MobiusDW",
    "propagator1.fermionaction.linksmear": "WilsonFlow",
    "propagator1.gaugeconfig": "Nf211",
    "propagator1.gaugeconfig.light": "Hisq",
    "propagator1.gaugeconfig.light.linksmear": "WilsonFlow",
    "propagator1.gaugeconfig.strange": "Hisq",
    "propagator1.gaugeconfig.strange.linksmear": "WilsonFlow",
    "propagator1.gaugeconfig.charm": "Hisq",
    "propagator1.gaugeconfig.charm.linksmear": "WilsonFlow",
    "propagator1.gaugeconfig.gaugeaction": "LuescherWeisz",
    "propagator1.sourcesmear": "GaugeCovariantGaussian",
    "propagator1.sinksmear": "Point",
    # p2
    "propagator2": "OneToAll",
    "propagator2.fermionaction": "MobiusDW",
    "propagator2.fermionaction.linksmear": "WilsonFlow",
    "propagator2.gaugeconfig": "Nf211",
    "propagator2.gaugeconfig.light": "Hisq",
    "propagator2.gaugeconfig.light.linksmear": "WilsonFlow",
    "propagator2.gaugeconfig.strange": "Hisq",
    "propagator2.gaugeconfig.strange.linksmear": "WilsonFlow",
    "propagator2.gaugeconfig.charm": "Hisq",
    "propagator2.gaugeconfig.charm.linksmear": "WilsonFlow",
    "propagator2.gaugeconfig.gaugeaction": "LuescherWeisz",
    "propagator2.sourcesmear": "GaugeCovariantGaussian",
    "propagator2.sinksmear": "Point",
    # Wave
    "sourcewave": "Hadron",
    "sinkwave": "Hadron",
}


def get_pars(
    key: str, parity: int = 1, isospin_z_x2: int = 1, spin_z_x2: int = 1
) -> Dict[str, Any]:
    parameters = {**global_pars, **special_pars}

    parameters.update(parse_propagator(key))

    parameters["naik"] = parameters.pop("light__naik")
    parameters.pop("strange__naik")
    parameters.pop("charm__naik")

    for n in range(3):
        parameters[f"propagator{n}.fermionaction.quark_mass"] = parameters[
            "MobiusDWF__quark_mass"
        ]

        for q in ["light", "strange", "charm"]:
            parameters[f"propagator{n}.gaugeconfig.{q}.quark_mass"] = parameters[
                f"{q}__quark_mass"
            ]

    parameters.pop("MobiusDWF__quark_mass")
    for q in ["light", "strange", "charm"]:
        parameters.pop(f"{q}__quark_mass")

    parameters["parity"] = parity
    parameters["isospin_z_x2"] = isospin_z_x2
    parameters["spin_z_x2"] = spin_z_x2

    return parameters


for key, parity, spin_z_x2 in tqdm(list(product(data, [-1, 1], [-1, 1]))):
    isospin_z_x2 = 1
    parameters = get_pars(key, parity, isospin_z_x2, spin_z_x2)

    ### for devel db only
    # pushes only partial dataset
    if int(parameters["config"]) < 401:
        pass
    else:
        continue

    b, created = Baryon2pt.get_or_create_from_parameters(
        parameters=parameters, tree=tree
    )
    b.tag = "proton"
    b.save()
