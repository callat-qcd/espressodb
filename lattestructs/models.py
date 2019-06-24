# pylint: disable=C0111, R0903, E1101
"""Lattice structure tables
"""
from django.db import models


class Source(models.Model):
    """Source class
    """

    gauge_id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"Source(gauge_id={self.gauge_id})"


class Action(models.Model):
    """
    """

    source = models.ForeignKey(Source, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.__class__.__name__}(gauge_id={self.source.gauge_id})"


class Hisq(Action):
    """
    """


class Clover(Action):
    """
    """


class GaugeConfiguration(models.Model):
    """
    """

    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    hisq = models.ForeignKey(Hisq, on_delete=models.CASCADE)
    clover = models.ForeignKey(Clover, on_delete=models.CASCADE)

    def clean(self):
        """Checks whether actions have same id as source
        """
        if not self.source == self.hisq.source == self.clover.source:
            raise ValueError(
                "Can only save gauge configuration if hisq and clover have the same"
                " source."
            )

    def __str__(self):
        return (
            f"GaugeConfiguration("
            f"gauge_id={self.source.gauge_id},"
            f" hisq,"
            f" clover)"
        )
