from django.db import models

from lattedb.base.models import Base


class HadronSmear(Base):
    """ Base table for application
    """

    description = models.TextField(
        null=True,
        blank=True,
        help_text="(Optional) Text: Description of the interpolating operator",
    )


class Unsmeared(HadronSmear):
    """
    Table for unsmeared operators.
    The table should only have one row with a foreign key.
    """


class Gaussian(HadronSmear):
    """ Gauge invariant Gaussian smearing
    """

    radius = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        help_text="Decimal(10,6): Smearing radius in lattice units",
    )
    step = models.PositiveSmallIntegerField(
        help_text="PositiveSmallInt: Number of smearing steps"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["radius", "step"], name="unique_hadronsmear_gaussian"
            )
        ]
