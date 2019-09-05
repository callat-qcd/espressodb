from lattedb.project.fhcompare.models.data import SourceAvg2pt
from lattedb.correlator.models import Baryon2pt
from lattedb.ensemble.models import Ensemble

# user defined
ensemble_label = ["a15m310L_a_21", "a12m310_a_21", "a09m310_e_17"] # latte-devel dataset
#ensemble_label = ["a15m310L_a_1000", "a12m310_a_1053", "a09m310_e_784"]

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

    for conf in configs:
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
                    data = SourceAvg2pt.objects.create()
                    data.baryon2pts.add(*corr_spin_parity)
                    data.save()
                    print("row inserted")
