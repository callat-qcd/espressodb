from django.db import models

from lattedb.base.models import Base


class GaugeConfig(Base):
    """ Base table for application
    """

    short_tag = models.TextField(
        null=True,
        blank=True,
        help_text="(Optional) Text: Short name for gaugeconfig (e.g. 'a15m310')",
    )
    stream = models.TextField(
        null=False, blank=False, help_text="Text: Stream tag for Monte Carlo"
    )
    config = models.PositiveSmallIntegerField(
        help_text="PositiveSmallInt: Configuration number"
    )
    gaugeaction = models.ForeignKey(
        "gaugeaction.GaugeAction",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey pointing to lattice gauge action",
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
    gaugesmear = models.ForeignKey(
        "gaugesmear.GaugeSmear",
        on_delete=models.CASCADE,
        help_text="ForeignKey pointing to additional gauge link smearing outside of Monte Carlo.",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "stream",
                    "config",
                    "gaugeaction",
                    "nx",
                    "ny",
                    "nz",
                    "nt",
                    "gaugesmear",
                    "type",
                ],
                name="unique_gaugeconfig",
            )
        ]

    def same_ensemble(self, config: "GaugeConfig") -> bool:
        """Checks if all meta information for a given config are the same.
        """
        equal = False
        if self.type == config.type:
            equal = all(
                [
                    getattr(self, column) == getattr(config, column)
                    for column in self.get_open_fields()
                    if column != "config"
                ]
            )

        return equal


class Nf211(GaugeConfig):
    """
    """

    light = models.ForeignKey(
        "fermionaction.FermionAction",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey pointing to lattice fermion action",
    )
    strange = models.ForeignKey(
        "fermionaction.FermionAction",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey pointing to lattice fermion action",
    )
    charm = models.ForeignKey(
        "fermionaction.FermionAction",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="ForeignKey pointing to lattice fermion action",
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
                fields=["gaugeconfig_ptr_id", "light", "strange", "charm"],
                name="unique_gaugeconfig_nf211",
            )
        ]
