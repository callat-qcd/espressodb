# pylint: disable=C0103
"""Example models to test check consistency methods of the many to many signals
"""
from typing import List, Optional
from django.db import models
from espressodb.base.models import Base


class A(Base):
    """Blank table with no columns
    """

    def __str__(self):
        return f"A(pk={self.pk})"

    def __repr__(self):
        return str(self)


class B(Base):
    """First many to many class
    """

    a_set = models.ManyToManyField(A)

    def __str__(self):
        return f"B(pk={self.pk})"

    def __repr__(self):
        return str(self)


class C(Base):
    """First class with two many to many fields
    """

    a_set = models.ManyToManyField(A)
    b_set = models.ManyToManyField(B)

    def __str__(self):
        return f"C(pk={self.pk})"

    def __repr__(self):
        return str(self)


class D(Base):
    """Many to many class which complains about having too many entries of a.
    """

    a_set = models.ManyToManyField(A)

    def __str__(self):
        return f"B(pk={self.pk})"

    def __repr__(self):
        return str(self)

    def check_m2m_consistency(
        self, instances: List["Base"], column: Optional[str] = None
    ):
        """Raises error if adding more than one instance of A at a time."""
        print(column, instances)
        if column == "a_set" and len(instances) > 1:
            print("errors")
            raise ValueError("I just want to have one entry of A at a time.")
