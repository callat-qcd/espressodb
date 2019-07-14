from django.db import models

from lattedb.base.models import Base


class HadronSmear(Base):
    """ Base table for application
    """

    description = models.TextField(
        null=False,
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
        max_digits=20,
        decimal_places=10,
        help_text="Decimal(20,10): Smearing radius in lattice units",
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