from django.db import models

from lattedb.base.models import Base

class Current(Base):
    """ Base table for application
    """

class Local(Current):
    """
    """
    diracstruct = models.CharField(
        max_length=20,
        null=False,
        blank=False,
        help_text="Char(20): Dirac structure of the current",
    )

    flavor0 = models.CharField(
        max_length=1,
        null=False,
        blank=True,
        help_text="(Optional) Char(1): Incoming quark field flavor. Useful to specify for nucleons.",
    )

    flavor1 = models.CharField(
        max_length=1,
        null=False,
        blank=True,
        help_text="(Optional) Char(1): Outgoing quark field flavor. Useful to specify for nucleons.",
    )

    description = models.TextField(
        null=False, blank=True, help_text="(Optional) Text: Description of current"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["diracstruct", "flavor0", "flavor1"],
                name="unique_current_local",
            )
        ]
