from django.db import models

from lattedb.status.models.base import FileStatus
from lattedb.correlator.models import Baryon2pt as _Baryon2pt


class Baryon2pt(FileStatus):
    baryon2pt = models.ForeignKey(
        _Baryon2pt,
        on_delete=models.CASCADE,
        null=False,
        help_text="ForeignKey: Baryon two point correlation function",
    )
    source_group = models.PositiveSmallIntegerField(
        null=True, help_text="PositiveSmallInt: Index to the source group"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["baryon2pt", "home"], name="unique_baryon2pt_file_status"
            )
        ]

    @classmethod
    def get_from_ensemble(
        cls,
        ensemble: "Ensemble",
        propagator: str = "propagator0",
        propagator_type: str = "OneToAll",
    ) -> "QuerySet(Baryon2pt)":
        """Returns all correlators which are associated with the ensemble.

        The association is given through the propagator relation.

        **Arguments**
            ensemble: Ensemble
                The ensemble of gaugeconfigs

            propagator: str = "propagator0"
                The propagator of the correlator associated with the gagugeconfig.
                For this correlator, can be one out of
                `[propagator0, propagator1, propagator2]`, but all should be on the same
                gaugeconfig anyway.

            propagator_type: str = "OneToAll"
                The type of the propagator e.g. "OneToAll".
        """
        baryon2pts = _Baryon2pt.get_from_ensemble(
            ensemble, propagator=propagator, propagator_type=propagator_type
        )
        return cls.objects.filter(baryon2pt__in=baryon2pts)
