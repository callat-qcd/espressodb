"""For this app the DB migrations are ahead of the local model (and migrations)
"""

# Note: if you want your models to use espressodb features, they must inherit from Base

from django.db import models
from espressodb.base.models import Base


class A1(Base):
    i = models.IntegerField()
