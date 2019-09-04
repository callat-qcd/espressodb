from django.db import models


class Data(models.Model):
    """Abstract base table for data
    """

    class Meta:
        abstract = True


class Project(models.Model):
    """Abstract base table for projects
    """

    class Meta:
        abstract = True
