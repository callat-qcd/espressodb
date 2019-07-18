from django.db import models

from lattedb.base.models import Base


class Ensemble(Base):
    """ Base table for application
    """

    short_tag = models.TextField(
        null=True,
        blank=True,
        help_text="(Optional) Text: Short name for ensemble (e.g. 'a15m310')",
    )
    stream = models.TextField(
        null=False, blank=False, help_text="Text: Stream tag for Monte Carlo"
    )
    nconfig = models.PositiveSmallIntegerField(
        help_text="PositiveSmallInt: Number of configurations"
    )
    action = models.ForeignKey(
        "action.Action",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey pointing to lattice action",
    )
    nx = models.PositiveSmallIntegerField(
        null=False, help_text="PositiveSmallInt: Spatial length in lattice units"
    )
    ny = models.PositiveSmallIntegerField(
        null=False, help_text="PositiveSmallInt: Spatial length in lattice units"
    )
    nz = models.PositiveSmallIntegerField(
        null=False, help_text="PositiveSmallInt: Spatial length in lattice units"
    )
    nt = models.PositiveSmallIntegerField(
        null=False, help_text="PositiveSmallInt: Temporal length in lattice units"
    )
    l_fm = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=True,
        help_text="(Optional) Decimal(10,6): Spatial length in fermi",
    )
    gaugesmear = models.ForeignKey(
        "gaugesmear.GaugeSmear",
        on_delete=models.CASCADE,
        help_text="ForeignKey pointing to gauge link smearing",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "stream",
                    "nconfig",
                    "action",
                    "nx",
                    "ny",
                    "nz",
                    "nt",
                    "gaugesmear",
                ],
                name="unique_ensemble",
            )
        ]


class Flavor211(Ensemble):
    """
    """
    ml = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=False,
        help_text="Decimal(10,6): Input light quark mass",
    )
    ms = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=False,
        help_text="Decimal(10,6): Input strange quark mass",
    )
    mc = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=False,
        help_text="Decimal(10,6): Input charm quark mass",
    )
    mpil = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=True,
        help_text="(Optional) Decimal(10,6): Spatial length in mpiL",
    )
    mpi = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=True,
        help_text="(Optional) Decimal(10,6): Pion mass in MeV",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["ensemble_ptr_id", "ml", "ms", "mc"],
                name="unique_ensemble_flavor211",
            )
        ]
