from django.db import models

from lattedb.base.models import Base

class GaugeSmear(Base):
    """ Base table for application"
    """

class Unsmeared(GaugeSmear):
    """
    """


class WilsonFlow(GaugeSmear):
    """
    """
    flowtime = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        help_text="Decimal(3,2): Flow time in lattice units",
    )

    steps = models.PositiveSmallIntegerField(
        help_text="PositiveSmallInt: Number of steps"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["flowtime", "steps"], name="unique_gaugesmear_wilsonflow"
            )
        ]
