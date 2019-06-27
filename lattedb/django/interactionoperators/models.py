from django.db import models
from lattedb.django.base.models import InteractionOperators

# Create your models here.
class LocalCurrents(InteractionOperators):
    """
    """

    diracstructure = models.CharField(
        max_length=20,
        null=False,
        blank=False,
        help_text="Char(20): Dirac structure of the current",
    )
    inflavor = models.CharField(
        max_length=1,
        null=False,
        blank=False,
        help_text="Char(1): Incoming quark field flavor",
    )
    outflavor = models.CharField(
        max_length=1,
        null=False,
        blank=False,
        help_text="Char(1): Outgoing quark field flavor",
    )
    description = models.TextField(
        null=False, blank=True, help_text="(Optional) Text: Description of current"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["diracstructure", "inflavor", "outflavor"],
                name="unique_localcurrents",
            )
        ]


class ConservedCurrents(InteractionOperators):
    """
    """


class SpatialMoments(InteractionOperators):
    """
    """


class PartonDistributionFunctions(InteractionOperators):
    """
    """
