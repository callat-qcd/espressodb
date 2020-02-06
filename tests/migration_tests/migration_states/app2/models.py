"""For this model, not all model fields are present in migrations
"""
# Note: if you want your models to use espressodb features, they must inherit from Base

from django.db import models
from espressodb.base.models import Base


class A1(Base):
    i = models.IntegerField()
    j = models.IntegerField(default=1)
