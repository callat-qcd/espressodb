from django.db import models

from lattedb.base.models import Base


class GaugeConfig(Base):
    """ Base table for application
    """

    def same_ensemble(self, config: "GaugeConfig") -> bool:
        """Checks if all meta information for a given config are the same.
        """
        equal = False
        if self.type == config.type:
            equal = all(
                [
                    getattr(self, column.name) == getattr(config, column.name)
                    for column in self.get_open_fields()
                    if column.name != "config"
                ]
            )

        return equal


class Nf211(GaugeConfig):
    """
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
                fields=[
                    "stream",
                    "config",
                    "gaugeaction",
                    "nx",
                    "ny",
                    "nz",
                    "nt",
                    "gaugesmear",
                    "light",
                    "strange",
                    "charm",
                ],
                name="unique_gaugeconfig_nf211",
            )
        ]

    @property
    def long_tag(self) -> str:
        """Returns descriptive long tag representing configuration
        """
        return (
            f"l{self.nx}{self.nt}"  # pylint: disable=E1101
            f"f211"
            f"b{int(self.gaugeaction.specialization.beta * 100)}"
            f"m{int(self.light.specialization.quark_mass*1000):03d}"
            f"m{int(self.strange.specialization.quark_mass*1000):03d}"
            f"m{int(self.charm.specialization.quark_mass*1000):03d}"
        )
