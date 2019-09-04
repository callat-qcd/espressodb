from django.db import models

from lattedb.status.models.base import FileStatus
from lattedb.correlator.models import Baryon2pt as Baryon2ptCorrelator


class Baryon2pt(FileStatus):
    barryon2pt = models.ForeignKey(
        Baryon2ptCorrelator,
        on_delete=models.CASCADE,
        null=False,
        help_text="ForeignKey: Baryon two point correlation function",
    )
    source_group = models.PositiveSmallIntegerField(
        null=True, help_text="PositiveSmallInt: Index to the source group"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["barryon2pt", "home"], name="unique_baryon2pt_file_status"
            )
        ]
