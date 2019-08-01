from django.db import models

from lattedb.base.models import Base


class Current(Base):
    """ Base table for application
    """


class Local(Current):
    """ Momentum space current
    """

    diracstruct = models.TextField(
        null=False, blank=False, help_text="Text: Dirac structure of the current"
    )

    momentum = models.SmallIntegerField(
        help_text="SmallInt: Current insertion momentum in units of 2 pi / L"
    )

    description = models.TextField(
        null=True, blank=True, help_text="(Optional) Text: Description of current"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["diracstruct", "momentum"], name="unique_current_local"
            )
        ]

class Local4D(Current):
    """ Spatial current
    """

    diracstruct = models.TextField(
        null=False, blank=False, help_text="Text: Dirac structure of the current"
    )

    description = models.TextField(
        null=True, blank=True, help_text="(Optional) Text: Description of current"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["diracstruct"], name="unique_current_local4d"
            )
        ]
