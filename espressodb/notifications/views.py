from django.shortcuts import render

from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from espressodb.notifications.models import Notification


class NotificationsView(LoginRequiredMixin, ListView):
    login_url = "/login/"

    model = Notification
    paginate_by = 2
    template_name = "notification_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context
