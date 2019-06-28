from django.db import models
from lattedb.django.base.models import BootstrapIndices
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class HisqBootstrapIndices(BootstrapIndices):
    """
    """

    gaugeconfiguration = models.ForeignKey(
        "base.GaugeConfigurations",
        on_delete=models.CASCADE,
        help_text="ForeignKey pointing to gauge field",
    )

    sample = models.PositiveSmallIntegerField(
        help_text="PositiveSmallInt: Bootstrap index where draw = 0 returns original data"
    )

    mask = ArrayField(
        models.PositiveSmallIntegerField(),
        help_text="Array[PositiveSmallInt]: An array of randomly drawn",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["gaugeconfiguration", "sample"], name="unique_hisqbootstrapindices"
            )
        ]
