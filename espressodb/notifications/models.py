# pylint: disable=E1101
"""Implements notifications similar to logging with optional viewer restrictions

The purpose of this module is having logging like capabilities which can be accessed
in web views.
Mimicing logging messages, notifications have a content field, a timestamp and a level.
To have control over what might be displayed on web views, the notifications come with
additional optional features:

.. autosummary::
    Notification.title
    Notification.tag
    Notification.groups
    Notification.read_by

The notifications view will be rendered on default whenever a user is logged in.

------

.. autosummary::
    LEVELS
    Notification
    Notifier

------
"""
from typing import Optional
from typing import List

from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

#: The available notifications levels
LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR")


class Notification(models.Model):
    """Model which implements logging like notification interface.

    The model is ordered according to `timestamp` in descending order.
    """

    #: (:class:`models.CharField`) - The title of the notification
    title = models.CharField(
        max_length=200, help_text="The title of the notification", null=True, blank=True
    )
    #: (:class:`models.TextField`) - The content of the notification
    content = models.TextField(help_text="The content of the notification")
    #: (:class:`models.CharField`) -
    #: The level of the notification mimicing logging levels. See also :data:`LEVELS`
    level = models.CharField(
        max_length=8,
        choices=[(level, level) for level in LEVELS],
        help_text="The level of the notification mimicing logging levels",
    )
    #: (:class:`models.CharField`) - A tag for fast searches
    tag = models.CharField(
        max_length=100, null=True, help_text="A tag for fast searches", blank=True
    )
    #: (:class:`models.ManyToManyField` -> :class:`django.contrib.auth.models.Group`) -
    #: The group of users who are allowed to read this notification
    groups = models.ManyToManyField(
        Group,
        blank=True,
        help_text="The group of users who are allowed to read this notification",
        related_name="notifications",
    )
    #: (:class:`models.DateTimeField`) -
    #: Creation date of the notification
    timestamp = models.DateTimeField(
        auto_now_add=True, help_text="Creation date of the notification"
    )
    #: (:class:`models.ManyToManyField` -> :class:`django.contrib.auth.models.User`) -
    #: The users who have read the notification
    read_by = models.ManyToManyField(
        User,
        blank=True,
        help_text="The users who have read the notification",
        related_name="read_notifications",
    )

    class Meta:  # pylint: disable=C0111, R0903
        ordering = ["-timestamp"]

    def add_user_to_read_by(self, user: User):
        """Adds the user to the :attr:`Notification.read_by` list and inserts in the db.

        Arguments:
            user: The user to check.
        """
        if not self.has_been_read_by(user):
            self.read_by.add(user)
            self.save()

    def has_been_read_by(self, user: User) -> bool:
        """Checks if the user has read the notification
        """
        return self.read_by.filter(pk=user.pk).exists()  # pylint: disable=E1101

    def viewable_by(self, user: Optional[User]) -> bool:
        """Checks if the user is allowed to read this notification.

        Arguments:
            user: The user to check.

        Returns:
            False if the notification groups are not empty and user is not in the
            specified groups.
        """
        allowed_to_read = True
        if self.groups.exists():  # pylint: disable=E1101
            if not Group.objects.intersection(user.groups, self.groups).exists():
                allowed_to_read = False
        return allowed_to_read

    @classmethod
    def get_notifications(
        cls, user: User, level: Optional[str] = None, show_all: bool = False
    ) -> List["Notification"]:
        """Returns all notifications the user is allowed to see.

        Arguments:
            user:
                The user who wants to see notifications
            level:
                The notification level to specialize.
                Shows notifications for all levels if not specified.
            show_all:
                If True also shows already read messages

        Results are order by timestamp in decreasing order.
        """
        general_notifications = cls.objects.filter(groups=None)

        if user.groups.exists():
            specific_notifications = cls.objects.filter(groups__in=user.groups.all())
        else:
            specific_notifications = cls.objects.none()

        notifications = general_notifications | specific_notifications

        if not show_all:
            notifications = notifications.exclude(read_by=user)

        if level and level in LEVELS:
            notifications = notifications.filter(level=level)

        return notifications.order_by("-timestamp")


class Notifier:
    """Logger like object which interactions with the Notification model.

    Example:
        .. code::

            notifier = Notifier(tag="my_app", groups=["admin"])
            notifer.debug("Set up notifier")
            notifier.info("Start to invesitgate app")
            ...
            notifier.error("ERROR! read this ...", title="NEED urgent attention!")

        Note that ``tag`` and ``groups`` can be overwriten by the kwargs of the notifier
        methods, e.g., ``notifer.debug("Set up notifier", tag="set up")``

    """

    _keys = ("tag", "groups")

    def __init__(self, tag: Optional[str] = None, groups: Optional[List[str]] = None):
        """Init the Notifier class

        Arguments:
            tag:
                The tag of the notification. Used for fast searches.
            groups:
                The user groups which are allowed to view this notfication.
                No groups means not logged in users are able to view the notfication.
        """
        #: The tag of the notification. Used for fast searches.
        self.tag = tag
        #: The user groups which are allowed to view this notfication.
        #: No groups means not logged in users are able to view the notfication.
        self.groups = self.get_groups_from_names(groups) if groups else []

    @staticmethod
    def get_groups_from_names(group_names: List[str]) -> List[Group]:
        """Parses the group names to :class:`Groups`.

        Arguments:
            group_names:
                List of group names which will be converted to a list of
                :class:`espressodb.notifications.models.Notification`.

        Raises:
            KeyError:
                If not all groups are found.
        """
        groups = Group.objects.filter(name__in=group_names)

        if groups.count() != len(group_names):
            missing_groups = set(group_names).difference(
                {groups.name for group in groups}
            )
            raise KeyError(
                "Could not locate all groups requested."
                f" The requested groups are {group_names},"
                f" but did not find {missing_groups}"
            )

        return groups

    def debug(
        self,
        content: str,
        title: Optional[str] = None,
        tag: Optional[str] = None,
        groups: Optional[List[str]] = None,
    ) -> Notification:
        """Creates notification at debug level.

        Arguments:
            content:
                The content of the notification
            title:
                The title of the notification
            tag:
                The tag of the notification. Used for fast searches.
                Overrides Notifier default tag.
            groups:
                The user groups which are allowed to view this notfication.
                No groups means not logged in users are able to view the notfication.
                Overrides Notifier default groups.

        Raises:
            KeyError:
                If groups are present but not found.
        """
        return self._create_notification(
            content=content, title=title, tag=tag, groups=groups, level="DEBUG"
        )

    def info(
        self,
        content: str,
        title: Optional[str] = None,
        tag: Optional[str] = None,
        groups: Optional[List[str]] = None,
    ) -> Notification:
        """Creates notification at info level.

        Arguments:
            content:
                The content of the notification
            title:
                The title of the notification
            tag:
                The tag of the notification. Used for fast searches.
                Overrides Notifier default tag.
            groups:
                The user groups which are allowed to view this notfication.
                No groups means not logged in users are able to view the notfication.
                Overrides Notifier default groups.

        Raises:
            KeyError:
                If groups are present but not found.
        """
        return self._create_notification(
            content=content, title=title, tag=tag, groups=groups, level="INFO"
        )

    def warning(
        self,
        content: str,
        title: Optional[str] = None,
        tag: Optional[str] = None,
        groups: Optional[List[str]] = None,
    ) -> Notification:
        """Creates notification at warning level.

        Arguments:
            content:
                The content of the notification
            title:
                The title of the notification
            tag:
                The tag of the notification. Used for fast searches.
                Overrides Notifier default tag.
            groups:
                The user groups which are allowed to view this notfication.
                No groups means not logged in users are able to view the notfication.
                Overrides Notifier default groups.

        Raises:
            KeyError:
                If groups are present but not found.
        """
        return self._create_notification(
            content=content, title=title, tag=tag, groups=groups, level="WARNING"
        )

    def error(
        self,
        content: str,
        title: Optional[str] = None,
        tag: Optional[str] = None,
        groups: Optional[List[str]] = None,
    ) -> Notification:
        """Creates notification at error level.

        Arguments:
            content:
                The content of the notification
            title:
                The title of the notification
            tag:
                The tag of the notification. Used for fast searches.
                Overrides Notifier default tag.
            groups:
                The user groups which are allowed to view this notfication.
                No groups means not logged in users are able to view the notfication.
                Overrides Notifier default groups.

        Raises:
            KeyError:
                If groups are present but not found.
        """
        return self._create_notification(
            content=content, title=title, tag=tag, groups=groups, level="ERROR"
        )

    def _create_notification(self, **kwargs) -> Notification:
        """Creates a notification entry in the db.

        Arguments:
            content:
                The content of the notification
            title:
                The title of the notification
            level:
                The level of the notification.
            tag:
                The tag of the notification. Used for fast searches.
                Overrides Notifier default tag.
            groups:
                The user groups which are allowed to view this notfication.
                No groups means not logged in users are able to view the notfication.
                Overrides Notifier default groups.

        Raises:
            KeyError:
                If groups are present but not found.
        """
        options = kwargs.copy()
        options["tag"] = options.get("tag", None) or self.tag
        groups = options.pop("groups", None)
        groups = self.get_groups_from_names(groups) if groups else self.groups

        notification = Notification.objects.create(**options)  # pylint: disable=E1101
        notification.groups.add(*groups)

        return notification
