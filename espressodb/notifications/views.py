# pylint: disable=E1101, R0901
"""Views for notifications module.
"""
from typing import List
from typing import Union

from django.db.models import QuerySet

from django.http import Http404
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from django.views import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import ListView

from django.contrib.auth.mixins import LoginRequiredMixin

from espressodb.notifications.models import Notification


class NotificationsView(LoginRequiredMixin, ListView):
    """View which displays notifications for logged in user and level.
    """

    #: Redirect user to login page if not logged in
    login_url = "/login/"
    #: Model of ListView
    model = Notification
    #: Paginate pages by
    paginate_by = 20
    #: The template file
    template_name = "notification_list.html"
    #: Level of notifications to show.
    #: Must be one of :data:`espressodb.notifications.models.LEVELS`.
    #: Shows notifications for all levels if not specified.
    level = ""

    def get_context_data(self, *, object_list=None, **kwargs):
        """Parses context data of view.

        Sets context view ``level`` to own view level.
        Sets context ``all`` option to true if specified as url parameter.
        """
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["level"] = self.level
        context["all"] = self.request.GET.get("all", "False").lower() == "true"
        return context

    def get_queryset(self) -> Union[QuerySet, List[Notification]]:
        """Returns notifications which are vieawable by logged in user for current level.
        """
        user = self.request.user
        show_all = self.request.GET.get("all", "False").lower() == "true"
        return Notification.get_notifications(user, self.level, show_all)


class HasReadView(LoginRequiredMixin, SingleObjectMixin, View):
    """Post only view to add logged in user to has read list of notification.
    """

    #: Model of SingleObjectMixin
    model = Notification
    #: Go back to notification list view on success
    success_url = reverse_lazy("notifications:notifications-list")

    @staticmethod
    def get(request, *args, **kwargs):
        """Get accessed of view is removed.

        Raises:
            Http404:
                When this function is called.
        """
        raise Http404("This site does not exist")

    def post(  # pylint: disable=W0613
        self, request, *args, **kwargs
    ) -> HttpResponseRedirect:
        """Adds logged in user to read_by list of notfication if user is allowed to see
        it.

        Raises:
            Http404:
                If user is not allowed to see notification.
        """
        notification = self.get_object()
        user = request.user

        if notification.viewable_by(user):
            notification.add_user_to_read_by(user)
        else:
            raise Http404("This site does not exist")

        return HttpResponseRedirect(self.success_url)
