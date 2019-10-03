# pylint: disable=E1101, R0901
"""
"""
from typing import Optional

from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from espressodb.notifications.models import Notification
from espressodb.notifications.models import LEVELS


class NotificationsView(LoginRequiredMixin, ListView):
    login_url = "/login/"

    model = Notification
    paginate_by = 20
    template_name = "notification_list.html"
    level = ""

    def get_context_data(self, *args, **kwargs):
        """
        """
        context = super().get_context_data(*args, **kwargs)
        context["level"] = self.level
        context["all"] = self.request.GET.get("all", "False").lower() == "true"
        return context

    def get_queryset(self):
        """
        """
        user = self.request.user
        show_all = self.request.GET.get("all", "False").lower() == "true"
        return Notification.get_notifications(user, self.level, show_all)


class HasReadView(LoginRequiredMixin, SingleObjectMixin, View):
    model = Notification
    success_url = reverse_lazy("notifications:notifications-list")

    @staticmethod
    def get(request, *args, **kwargs):
        """This view has no get view
        """
        raise Http404("This site does not exist")

    def post(self, request, *args, **kwargs):  # pylint: disable=W0613
        """
        """
        notification = self.get_object()
        user = request.user

        if notification.viewable_by(user):
            notification.add_user_to_read_by(user)
        else:
            raise Http404("This site does not exist")

        return HttpResponseRedirect(self.success_url)
