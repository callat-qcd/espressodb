"""Views for the base module
"""
from django.http import HttpResponse


def index(request):  # pylint: disable=W0613
    return HttpResponse("Hello, world. You're at the polls index.")
