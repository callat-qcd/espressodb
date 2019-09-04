from django.db import models

from lattedb.correlator.models import Baryon2pt
from lattedb.status.models import FileStatus


class Correlator_Baryon2pt(FileStatus):
    object = models.ForeignKey(
        Baryon2pt,
        on_delete=models.CASCADE,
        help_text="ForeignKey: Baryon two point correlation function",
    )
    source_group = models.PositiveSmallIntegerField(
        null=True, help_text="PositiveSmallInt: Index to the source group"
    )
