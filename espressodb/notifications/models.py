# pylint: disable=E1101
"""Implements notifications similar to logging with optional viewer restrictions
"""
from typing import Optional
from typing import List

from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR")

# Create your models here.
class Notification(models.Model):
    """Model which implements logging like notification module
    """

    title = models.CharField(
        max_length=200, help_text="The title of the notification", null=True, blank=True
    )
    content = models.TextField(help_text="The content of the notification")
    level = models.CharField(
        max_length=8,
        choices=[(level, level) for level in LEVELS],
        help_text="The level of the notification mimicing logging levels",
    )
    tag = models.CharField(
        max_length=100, null=True, help_text="A tag for fast searches", blank=True
    )
    groups = models.ManyToManyField(
        Group,
        blank=True,
        help_text="The group of users how are allowed to read this notification",
        related_name="notifications",
    )
    timestamp = models.DateTimeField(
        auto_now_add=True, help_text="Creation date of the notification"
    )
    read_by = models.ManyToManyField(
        User,
        blank=True,
        help_text="The users who have read the notification",
        related_name="read_notifications",
    )

    class Meta:  # pylint: disable=C0111, R0903
        ordering = ["-timestamp"]

    def add_user_to_read_by(self, user: User):
        """Adds the user to the read_by list and inserts in the db.
        """
        if not self.has_been_read_by(user):
            self.read_by.add(user)
            self.save()

    def has_been_read_by(self, user: User):
        """Checks if the user has read the notification
        """
        return self.read_by.filter(pk=user.pk).exists()  # pylint: disable=E1101

    def viewable_by(self, user: Optional[User]):
        """Checks if the user is allowed to read this notification.

        Returns False if the notification groups are not empty and user is not in the
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

        :param user: The user who wants to see notifications
        :param level: The notification level to specialize
        :param show_all: If True also shows already read messages

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
    """Logger like object to set notifications

    :ivar tag: The tag of the notification. Used for fast searches.
    :ivar groups: The user groups which are allowed to view this notfication.
        No groups means not logged in users are able to view the notfication.
    :ivar fail_if_not_exists: If the user specifies group names which are not found,
        the default behavior is that storing of notfications will fail
        (e.g., raising KeyErrors).
        If this is set to False, the code progress but logs Notifications to other
        groups.

    .. admonition:: Example

        ```
        notifier = Notifier(tag="my_app", groups=["admin"])
        notifer.debug("Set up notifier")
        notifier.info("Start to invesitgate app")
        ...
        notifier.error("Here is the error message ...", title="NEED urgent attention!")
        ```

    .. Note:

        Note that `tag` and `groups` can be overwriten by the kwargs of the notifier
        methods, e.g., ``notifer.debug("Set up notifier", tag="set up")``

    """

    _keys = ("tag", "groups")

    def __init__(
        self,
        tag: Optional[str] = None,
        groups: Optional[List[str]] = None,
        fail_if_not_exists: bool = True,
    ):
        """Init the Notifier class

        :param tag: The tag of the notification. Used for fast searches.
        :param groups: The user groups which are allowed to view this notfication.
            No groups means not logged in users are able to view the notfication.
        :param fail_if_not_exists: If the user specifies group names which are not found,
            the default behavior is that storing of notfications will fail
            (e.g., raising KeyErrors).
            If this is set to False, the code progress but logs Notifications to other
            groups.

        """
        self.tag = tag
        self.groups = self.get_groups_from_names(groups) if groups else []
        self.fail_if_not_exists = fail_if_not_exists

    def get_groups_from_names(self, group_names: List[str]) -> List[Group]:
        """Parses the group names to actual groups

        :param group_names: List of group names which will be converted to a list of
                :class:`espressodb.notifications.models.Notification`.

        Raises KeyError if `fail_if_not_exists` is True and not all groups are found.
        Else returns found groups.
        """
        groups = Group.objects.filter(name__in=group_names)

        if self.fail_if_not_exists and groups.count() != len(group_names):
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
        """Creates a debug notification

        :param content: The content of the notification
        :param title: The title of the notification
        :param tag: The tag of the notification. Used for fast searches.
        :param groups: The user groups which are allowed to view this notfication.
            No groups means not logged in users are able to view the notfication.
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
        """Creates an info notification

        :param content: The content of the notification
        :param title: The title of the notification
        :param tag: The tag of the notification. Used for fast searches.
        :param groups: The user groups which are allowed to view this notfication.
            No groups means not logged in users are able to view the notfication.
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
        """Creates a warning notification

        :param content: The content of the notification
        :param title: The title of the notification
        :param tag: The tag of the notification. Used for fast searches.
        :param groups: The user groups which are allowed to view this notfication.
            No groups means not logged in users are able to view the notfication.
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
        """Creates a error notification

        :param content: The content of the notification
        :param title: The title of the notification
        :param tag: The tag of the notification. Used for fast searches.
        :param groups: The user groups which are allowed to view this notfication.
            No groups means not logged in users are able to view the notfication.
        """
        return self._create_notification(
            content=content, title=title, tag=tag, groups=groups, level="ERROR"
        )

    def _create_notification(self, **kwargs) -> Notification:
        """Creates a notification entry in the db.

        :param content: The content of the notification
        :param title: The title of the notification.
        :param tag: The tag of the notification. Used for fast searches.
        :param level: The level of the notification.
            Should be one of :py:const:`espressodb.notifications.models.LEVELS`.
        :param groups: The user groups which are allowed to view this notfication.
            No groups means not logged in users are able to view the notfication.
        """
        options = kwargs.copy()
        options["tag"] = options.get("tag", None) or self.tag
        groups = options.pop("groups", None)
        groups = self.get_groups_from_names(groups) if groups else self.groups

        notification = Notification.objects.create(**options)  # pylint: disable=E1101
        notification.groups.add(*groups)

        return notification
