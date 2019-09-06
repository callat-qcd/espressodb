from django.db import models

from lattedb.base.models import Base

STATUS_CHOICES = (
    (0, ("Unknown")),
    (1, ("Does not exist")),
    (2, ("Exists")),
    (3, ("On tape")),
)


class FileStatus(Base):
    """ Base table for application
    """

    home = models.TextField(
        null=True,
        blank=True,
        help_text="(Optional) Text: Computing facility where the object resides at",
    )
    file_path = models.TextField(
        null=True, blank=True, help_text="(Optional) Text: Path to hdf5 file"
    )
    dset_path = models.TextField(
        null=True, blank=True, help_text="(Optional) Text: Path to dset in hdf5 file"
    )
    status = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="PositiveSmallInt: Encode categorical status labels",
        choices=STATUS_CHOICES,
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        help_text="DateTime:Last time the field was updated.",
    )

    class Meta:
        abstract = True
