from django.db import models

from lattedb.base.models import Base


class GaugeAction(Base):
    """ Base table for application
    """


class LuescherWeisz(GaugeAction):
    """
    """

    beta = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=False,
        help_text="Decimal(10,6): Coupling constant",
    )
    a_fm = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=True,
        help_text="(Optional) Decimal(10,6): Lattice spacing in fermi",
    )
    u0 = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=False,
        help_text="Decimal(10,6): Tadpole improvement coefficient",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["beta", "u0"], name="unique_gaugeaction_luescherweisz"
            )
        ]
