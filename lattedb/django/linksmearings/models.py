from django.db import models

from lattedb.django.base.models import LinkSmearings

# Create your models here.
class Unsmeared(LinkSmearings):
    """
    """


class WilsonFlow(LinkSmearings):
    """
    """

    flowtime = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        help_text="Decimal(3,2): Flow time in lattice units",
    )
