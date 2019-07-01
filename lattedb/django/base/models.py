# pylint: disable=C0111, R0903, E1101
"""Lattice structure tables
"""
from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField

from django_pandas.managers import DataFrameManager


class Base(models.Model):
    """
    """

    id = models.AutoField(primary_key=True)
    type = models.TextField(editable=False)  # autofield by inheritance
    last_modified = models.DateTimeField(auto_now=True)  # also update
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    objects = DataFrameManager()

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id})"

    class Meta:
        abstract = True

    def clean(self):
        """Sets the type name to the class instance name
        """
        self.type = self.__class__.__name__

    @classmethod
    def get_class_name(cls) -> str:
        """Returns the name of the class
        """
        return cls.__name__

    @classmethod
    def get_unique_class_name(cls) -> str:
        """Returns unique name which consist of it's own and parent class names.
        """
        parent = cls.__base__
        parent_name = (
            parent.get_unique_class_name() + "_" if parent is not models.Model else ""
        )
        return parent_name + cls.get_class_name()


class Status(Base):
    home = models.CharField(
        max_length=20,
        null=False,
        blank=True,
        help_text="(Optional) Char(20): Computing facility where the object resides at",
    )
    runscript = models.TextField(
        null=False,
        blank=True,
        help_text="(Optional) Text: Path to, or content of run script",
    )
    directory = models.TextField(
        null=False, blank=True, help_text="(Optional) Text: Path to result"
    )
    size = models.IntegerField(
        null=True, help_text="(Optional) Int: file size"
    )
    statusencoder = models.PositiveSmallIntegerField(
        help_text="PositiveSmallInt: Encode categorical status labels with values between 0 and n_classes-1"
    )

    class Meta:
        abstract = True


class GaugeConfig(Base):
    """
    """

    misc = JSONField(
        null=True, blank=True, help_text="(Optional) JSON: {'anything': 'you want'}"
    )


class Bootstrap(Base):
    """
    """

    misc = JSONField(
        null=True, blank=True, help_text="(Optional) JSON: {'anything': 'you want'}"
    )


class Propagator(Base):
    """
    """

    misc = JSONField(
        null=True, blank=True, help_text="(Optional) JSON: {'anything': 'you want'}"
    )


class GaugeSmear(Base):
    """
    """

    misc = JSONField(
        null=True, blank=True, help_text="(Optional) JSON: {'anything': 'you want'}"
    )


class HadronOp(Base):
    """
    """

    misc = JSONField(
        null=True, blank=True, help_text="(Optional) JSON: {'anything': 'you want'}"
    )


class CurrentOp(Base):
    """
    """

    misc = JSONField(
        null=True, blank=True, help_text="(Optional) JSON: {'anything': 'you want'}"
    )


class Correlator(Base):
    """
    """

    misc = JSONField(
        null=True, blank=True, help_text="(Optional) JSON: {'anything': 'you want'}"
    )

