from lattedb.project_fhcompare.models import Data_SourceAvg2pt
from lattedb.correlator.models import Correlator
from lattedb.ensemble.models import Ensemble

# user defined
ensemble_label = ["a15m310L_a_1000", "a12m310_a_1053", "a09m310_e_784"]

parity = [1, -1]
spin_z_x2 = [1, -1]

# code
for ens in ensemble_label:
    ensemble_meta = Ensemble.objects.get(label=ens)

    correlators = Correlator.objects.filter(type="Baryon2pt").filter(
        baryon2pt__propagator0__onetoall__gaugeconfig__in=ensemble_meta.configurations.all()
    )

    configs = (
        correlators.distinct()
        .order_by("baryon2pt__propagator0__onetoall__gaugeconfig__nf211__config")
        .values_list(
            "baryon2pt__propagator0__onetoall__gaugeconfig__nf211__config", flat=True
        )
    )

    for conf in configs[:2]:
        for sz in spin_z_x2:
            for par in parity:
                corr_spin_parity = (
                    correlators.filter(baryon2pt__propagator0__onetoall__gaugeconfig__nf211__config=conf)
                    .filter(baryon2pt__sink__hadron__parity=par)
                    .filter(baryon2pt__sink__hadron__spin_z_x2=sz)
                )

                print(corr_spin_parity.values("id"))
                print(corr_spin_parity.count())
