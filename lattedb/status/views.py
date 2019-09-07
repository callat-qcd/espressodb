from django.shortcuts import render
from django.urls import reverse_lazy

# Create your views here.

from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from lattedb.status.models.correlator import Baryon2pt as Baryon2ptStatus
from lattedb.ensemble.models import Ensemble


class Baryon2ptProgressView(LoginRequiredMixin, TemplateView):

    template_name = "progress.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = {
            "table": "Baryon2pt Status",
            "summary": {},
            "total": {},
            "class": "Baryon2pt Status",
            "subcategory": "Ensemble",
        }

        for ensemble in Ensemble.objects.all():
            sub_statuses = Baryon2ptStatus.get_from_ensemble(ensemble)

            context["summary"][
                ensemble.short_tag + " &nbsp;&nbsp; " + ensemble.long_tag
            ] = {
                "danger": sub_statuses.filter(status=1).count(),
                "warning": sub_statuses.filter(status=0).count(),
                "info": sub_statuses.filter(status=3).count(),
                "success": sub_statuses.filter(status=2).count(),
                "total": sub_statuses.count(),
            }

        return context
