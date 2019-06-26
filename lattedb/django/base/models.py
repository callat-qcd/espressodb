# pylint: disable=C0111, R0903, E1101
"""Lattice structure tables
"""
from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField


class Base(models.Model):
    """
    """

    id = models.AutoField(primary_key=True)
    type = models.TextField(editable=False)  # autofield by inheritance
    last_modified = models.DateTimeField(auto_now=True)  # also update
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id})"

    class Meta:
        abstract = True

    def clean(self):
        """Sets the type name to the class instance name
        """
        self.type = self.__class__.__name__


class GaugeConfig(Base):
    """
    """
    directory = models.TextField(
        null=False,
        blank=True,
        help_text="(Optional) Text: Directory path to gauge field",
    )
    misc = JSONField(
        null=True, blank=True, help_text="(Optional) JSON: {'anything': 'you want'}"
    )

class Propagators(Base):
    """
    """
    directory = models.TextField(
        null=False,
        blank=True,
        help_text="(Optional) Text: Directory path to propagator",
    )
    misc = JSONField(
        null=True, blank=True, help_text="(Optional) JSON: {'anything': 'you want'}"
    )

class LinkSmearings(Base):
    """
    """
    misc = JSONField(
        null=True, blank=True, help_text="(Optional) JSON: {'anything': 'you want'}"
    )

class InterpolatingOperators(Base):
    """
    """
    misc = JSONField(
        null=True, blank=True, help_text="(Optional) JSON: {'anything': 'you want'}"
    )

class InteractionOperators(Base):
    """
    """
    misc = JSONField(
        null=True, blank=True, help_text="(Optional) JSON: {'anything': 'you want'}"
    )