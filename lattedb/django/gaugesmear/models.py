from django.db import models
from django.contrib.postgres.fields import JSONField

from lattedb.django.base.models import Base

class GaugeSmear(Base):
    """ Base table for application"
    """

    misc = JSONField(
        null=True, blank=True, help_text="(Optional) JSON: {'anything': 'you want'}"
    )

class Unsmeared(GaugeSmear):
    """
    """


class WilsonFlow(GaugeSmear):
    """
    """

    tag = models.CharField(
        max_length=20,
        null=False,
        blank=True,
        help_text="(Optional) Char(20): User defined tag for easy searches",
    )

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
