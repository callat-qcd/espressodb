from django.db import models

from lattedb.django.base.models import LinkSmearing

# Create your models here.
class Unsmeared(LinkSmearing):
    """
    """


class WilsonFlow(LinkSmearing):
    """
    """

    flowtime = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        help_text="Decimal(3,2): Flow time in lattice units",
    )
