from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.fields import ArrayField

from lattedb.project.fhcompare.models.analysis import Fhcompare
from lattedb.correlator.models import Correlator


class Jason0(Fhcompare):
    """ Everyone should have their own table.
    Unique constraints are set on user-defined tables.
    """

    corr2pt = models.ForeignKey(
        "correlator.Correlator", on_delete=models.CASCADE, related_name="+"
    )

    corrseq = models.ManyToManyField(Correlator)

    listofcorrs = ArrayField(
        models.TextField(), default=list, help_text="Text: A list of correlators used"
    )

    trange = JSONField(
        null=False,
        blank=False,
        default=dict,
        help_text="Dictionary of time ranges, this goes into creating the hash",
    )

    states = JSONField(
        null=False,
        blank=False,
        default=dict,
        help_text="Dictionary of nstates, enters in hash",
    )

    inputs = JSONField(
        null=False,
        blank=False,
        default=dict,
        help_text="Other inputs (priors, etc...), enters in hash",
    )

    hash_fit = models.TextField(
        null=False,
        blank=False,
        default="",
        help_text="Unique hash field to prevent writing in same result",
    )

    # tmin2pt = models.SmallIntegerField(null=False)
    # tmax2pt = models.SmallIntegerField(null=False)
    # tminfhga = models.SmallIntegerField(null=False)
    # tmaxfhga = models.SmallIntegerField(null=False)
    # tminfhgv = models.SmallIntegerField(null=False)
    # tmaxfhgv = models.SmallIntegerField(null=False)
    # tminseqga = models.SmallIntegerField(null=False)
    # tmaxseqga = models.SmallIntegerField(null=False)
    # uminseqga = models.SmallIntegerField(null=False)
    # umaxseqga = models.SmallIntegerField(null=False)
    # tminseqgv = models.SmallIntegerField(null=False)
    # tmaxseqgv = models.SmallIntegerField(null=False)
    # uminseqgv = models.SmallIntegerField(null=False)
    # umaxseqgv = models.SmallIntegerField(null=False)
    # nstates = models.SmallIntegerField(null=False)
    # fstates = models.SmallIntegerField(null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "hash_fit",
                ],
                name="unique_project_fhcompare_jason0",
            )
        ]
