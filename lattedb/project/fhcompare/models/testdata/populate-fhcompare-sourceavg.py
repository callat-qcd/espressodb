from lattedb.project.fhcompare.models.data import SourceAvg2pt
from lattedb.correlator.models import Baryon2pt
from lattedb.ensemble.models import Ensemble

import h5py as h5
import pandas as pd

# user defined
ensemble_label = [
    "a15m310L_a_21",
    "a12m310_a_21",
    "a09m310_e_17",
]  # latte-devel dataset
# ensemble_label = ["a15m310L_a_1000", "a12m310_a_1053", "a09m310_e_784"]

head = {
    "a09m310": "gf1p0_w3p5_n45_M51p1_L56_a1p5",
    "a12m310": "gf1p0_w3p0_n30_M51p2_L58_a1p5",
    "a15m310": "gf1p0_w3p0_n30_M51p3_L512_a1p5",
}

hadron = ["proton", "proton_np"]

mass = {"a09m310": "ml0p00951", "a12m310": "ml0p0126", "a15m310": "ml0p0158"}

spin = ["spin_up", "spin_dn"]

parity = [1, -1]
spin_z_x2 = [1, -1]

# code
for ens in ensemble_label:
    ensemble_meta = Ensemble.objects.get(label=ens)

    baryon2pts = Baryon2pt.objects.filter(
        propagator0__onetoall__gaugeconfig__in=ensemble_meta.configurations.all()
    )

    configs = (
        baryon2pts.distinct()
        .order_by("propagator0__onetoall__gaugeconfig__nf211__config")
        .values_list("propagator0__onetoall__gaugeconfig__nf211__config", flat=True)
    )

    short_tag = ens.split("_")[0][:7]
    h5data = h5.File("./%s-devel.h5" % short_tag, "r")
    df = pd.DataFrame()
    for sz in spin_z_x2:
        for par in parity:
            if par == -1:
                paridx = 1
            else:
                paridx = 0
            cfgs_srcs = h5data[
                "%s/spec/%s/%s/px0_py0_pz0/cfgs_srcs"
                % (head[short_tag], mass[short_tag], hadron[paridx])
                ][()]
            corr = h5data["%s/spec/%s/%s/px0_py0_pz0/%s"
                          % (head[short_tag], mass[short_tag], hadron[paridx], sz)
                          ][()]


    for conf in configs[:2]:
        for sz in spin_z_x2:
            for par in parity:
                print(ens, conf, sz, par)
                corr_spin_parity = (
                    baryon2pts.filter(
                        propagator0__onetoall__gaugeconfig__nf211__config=conf
                    )
                    .filter(sink__hadron__parity=par)
                    .filter(sink__hadron__spin_z_x2=sz)
                )

                # print(corr_spin_parity.values_list("id", flat=True))
                # print(corr_spin_parity.count())

                data = SourceAvg2pt.objects.filter(
                    baryon2pts__in=corr_spin_parity.values_list("id")
                )
                if data.exists():
                    print("row exists... skipping")
                else:

                    data = SourceAvg2pt.objects.create(real=[1, 1], imag=[1, 1])
                    data.baryon2pts.add(*corr_spin_parity)

                    data.save()
                    print("row inserted")
