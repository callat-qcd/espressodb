from django.db import models
from lattedb.projects.fhcompare.models.analysis import Fhcompare


class Jason0(Fhcompare):
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
