from lattedb.django.base.models import Propagators
from django.db import models

# Create your models here.


class HisqPropagators(Propagators):
    """
    """

    tag = models.CharField(
        max_length=20,
        null=False,
        blank=True,
        help_text="(Optional) Char(20): User defined tag for easy searches",
    )

    gaugeconfiguration = models.ForeignKey(
        "base.GaugeConfigurations",
        on_delete=models.CASCADE,
        help_text="ForeignKey pointing to gauge field",
    )
    linksmearing = models.ForeignKey(
        "base.LinkSmearings",
        on_delete=models.CASCADE,
        help_text="ForeignKey pointing to link smearing",
    )
    mval = models.DecimalField(
        max_digits=7,
        decimal_places=6,
        null=False,
        help_text="Decimal(7,6): Input valence quark mass",
    )

    origin = models.TextField(
        null=False, blank=False, help_text="Text: Origin location of the propagator"
    )

    directory = models.TextField(
        null=False, blank=True, help_text="(Optional) Text: Directory path to propagator"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["gaugeconfiguration", "linksmearing", "mval", "origin"],
                name="unique_hisqpropagators",
            )
        ]


class MobiusPropagators(Propagators):
    """
    """

    tag = models.CharField(
        max_length=20,
        null=False,
        blank=True,
        help_text="(Optional) Char(20): User defined tag for easy searches",
    )
    gaugeconfiguration = models.ForeignKey(
        "base.GaugeConfigurations",
        on_delete=models.CASCADE,
        help_text="ForeignKey pointing to gauge field",
    )
    linksmearing = models.ForeignKey(
        "base.LinkSmearings",
        on_delete=models.CASCADE,
        help_text="ForeignKey pointing to link smearing",
    )
    mval = models.DecimalField(
        max_digits=7,
        decimal_places=6,
        null=False,
        help_text="Decimal(7,6): Input valence quark mass",
    )
    l5 = models.PositiveSmallIntegerField(
        help_text="PositiveSmallInt: Length of 5th dimension"
    )
    m5 = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=False,
        help_text="Decimal(3,2): 5th dimensional mass",
    )
    alpha5 = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=False,
        help_text="Decimal(3,2): Mobius coefficient [D_mobius(M5) = alpha5 * D_Shamir(M5)]",
    )
    a5 = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=False,
        help_text="Decimal(3,2): Mobius kernel parameter [D_mobius = alpha5 * a5 * D_Wilson / (2 + a5 * D_Wilson)]",
    )
    b5 = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=False,
        help_text="Decimal(3,2): Mobius kernel parameter [a5 = b5 - c5, alpha5 * a5 = b5 + c5]",
    )
    c5 = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=False,
        help_text="Decimal(3,2): Mobius kernal perameter",
    )

    origin = models.TextField(
        null=False, blank=False, help_text="Text: Origin location of the propagator"
    )

    directory = models.TextField(
        null=False, blank=True, help_text="(Optional) Text: Directory path to propagator"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "gaugeconfiguration",
                    "linksmearing",
                    "mval",
                    "l5",
                    "m5",
                    "alpha5",
                    "a5",
                    "b5",
                    "c5",
                    "origin",
                ],
                name="unique_mobiuspropagators",
            )
        ]


class CloverPropagators(Propagators):
    """
    """
