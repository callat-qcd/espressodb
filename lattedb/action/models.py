from django.db import models

from lattedb.base.models import Base


class Action(Base):
    """ Base table for application
    """

    beta = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=False,
        help_text="Decimal(10,6): Coupling constant",
    )
    a_fm = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=True,
        help_text="(Optional) Decimal(10,6): Lattice spacing in fermi",
    )


class Hisq(Action):
    """
    """

    naik = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=False,
        help_text="Decimal(10,6): Coefficient of Naik term. If Naik term is not included, explicitly set to 0",
    )
    u0 = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=True,
        help_text="Decimal(10,6): Tadpole improvement coefficient",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["action_ptr_id", "naik", "u0"], name="unique_action_hisq"
            )
        ]


class MobiusDW(Action):
    """
    """

    l5 = models.PositiveSmallIntegerField(
        help_text="PositiveSmallInt: Length of 5th dimension"
    )
    m5 = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=False,
        help_text="Decimal(10,6): 5th dimensional mass",
    )
    alpha5 = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=False,
        help_text="Decimal(10,6): Mobius coefficient [D_mobius(M5) = alpha5 * D_Shamir(M5)]",
    )
    a5 = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=False,
        help_text="Decimal(10,6): Mobius kernel parameter [D_mobius = alpha5 * a5 * D_Wilson / (2 + a5 * D_Wilson)]",
    )
    b5 = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=False,
        help_text="Decimal(10,6): Mobius kernel parameter [a5 = b5 - c5, alpha5 * a5 = b5 + c5]",
    )
    c5 = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=False,
        help_text="Decimal(10,6): Mobius kernal perameter",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["action_ptr_id", "l5", "m5", "alpha5", "a5", "b5", "c5"],
                name="unique_action_mobiusdw",
            )
        ]
