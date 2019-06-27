from lattedb.django.base.models import OperatorSmearings
from django.db import models


class GaugeInvariantGaussian(OperatorSmearings):
    tag = models.CharField(
        max_length=20,
        null=False,
        blank=True,
        help_text="(Optional) Char(20): User defined tag for easy searches",
    )
    nhits = models.PositiveSmallIntegerField(
        help_text="PositiveSmallInt: Number of smearing applications"
    )
    width =
