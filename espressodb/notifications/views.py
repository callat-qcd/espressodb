from django.shortcuts import render

from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from espressodb.notifications.models import Notfication


class NotificationsView(LoginRequiredMixin, ListView):

    model = Notfication
    paginate_by = 20
    template_name = "notification_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context
