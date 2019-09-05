from django.test import TestCase
from lattedb.project.fhcompare.models.data import SourceAvg2pt

# Create your tests here.
class Test(TestCase):
    def test_1(self):
        SourceAvg2pt.objects.all()