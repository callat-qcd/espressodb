from django.db import models

from lattedb.django.base.models import LinkSmearings

# Create your models here.
class Unsmeared(LinkSmearings):
    """
    """


class WilsonFlow(LinkSmearings):
    """
    """

    tag = models.CharField(
        max_length=20,
        null=False,
        blank=True,
        help_text='(Optional) Char(20): User defined tag for easy searches'
    )

    flowtime = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        help_text="Decimal(3,2): Flow time in lattice units",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["flowtime"], name="unique_wilsonflow")
        ]
