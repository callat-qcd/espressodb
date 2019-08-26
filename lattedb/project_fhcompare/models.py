from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.postgres.fields import JSONField

from lattedb.base.models import Base


class Project_Fhcompare(Base):
    """ Base table for application
    """

    mn = models.FloatField(null=False, help_text="Float: nucleon mass")

    ga = models.FloatField(null=False, help_text="Float: axial charge")

    gv = models.FloatField(null=False, help_text="Float: vector charge")

    rating = models.SmallIntegerField(
        null=False,
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Int: Limit from 1 to 5, default = 1. Rate your own fits.",
    )

    result = JSONField(
        null=False, blank=False, help_text="JSON: {'your_results': 'all dumped here'}"
    )


class Jason0(Project_Fhcompare):
    """ Everyone should have their own table.
    Unique constraints are set on user-defined tables.
    """

    corr2pt = models.ForeignKey(
        "correlator.Correlator", on_delete=models.CASCADE, related_name="+"
    )

    corrfhga = models.ForeignKey(
        "correlator.Correlator", on_delete=models.CASCADE, related_name="+"
    )

    corrfhgv = models.ForeignKey(
        "correlator.Correlator", on_delete=models.CASCADE, related_name="+"
    )

    corrseqga = models.ForeignKey(
        "correlator.Correlator", on_delete=models.CASCADE, related_name="+"
    )

    corrseqgv = models.ForeignKey(
        "correlator.Correlator", on_delete=models.CASCADE, related_name="+"
    )

    tmin2pt = models.SmallIntegerField(null=False)
    tmax2pt = models.SmallIntegerField(null=False)
    tminfhga = models.SmallIntegerField(null=False)
    tmaxfhga = models.SmallIntegerField(null=False)
    tminfhgv = models.SmallIntegerField(null=False)
    tmaxfhgv = models.SmallIntegerField(null=False)
    tminseqga = models.SmallIntegerField(null=False)
    tmaxseqga = models.SmallIntegerField(null=False)
    uminseqga = models.SmallIntegerField(null=False)
    umaxseqga = models.SmallIntegerField(null=False)
    tminseqgv = models.SmallIntegerField(null=False)
    tmaxseqgv = models.SmallIntegerField(null=False)
    uminseqgv = models.SmallIntegerField(null=False)
    umaxseqgv = models.SmallIntegerField(null=False)
    nstates = models.SmallIntegerField(null=False)
    fstates = models.SmallIntegerField(null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "corr2pt",
                    "corrfhga",
                    "corrfhgv",
                    "corrseqga",
                    "corrseqgv",
                    "tmin2pt",
                    "tmax2pt",
                    "tminfhga",
                    "tmaxfhga",
                    "tminfhgv",
                    "tmaxfhgv",
                    "tminseqga",
                    "tmaxseqga",
                    "uminseqga",
                    "umaxseqga",
                    "tminseqgv",
                    "tmaxseqgv",
                    "uminseqgv",
                    "umaxseqgv",
                    "nstates",
                    "fstates",
                ],
                name="unique_project_fhcompare_jason0",
            )
        ]
