from unittest.mock import patch

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse

from allianceauth.notifications import notify
from allianceauth.notifications.models import Notification
from allianceauth.services.modules.discord.models import DiscordUser

from . import views
from .signals import forward_new_notifications

CORE_PATH = "discordnotify.core"
SIGNALS_PATH = "discordnotify.signals"
VIEWS_PATH = "discordnotify.views"


@patch(CORE_PATH + "._send_message_to_discord_user")
@override_settings(CELERY_ALWAYS_EAGER=True)
class TestIntegration(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user("Bruce Wayne")

    @patch(SIGNALS_PATH + ".DISCORDNOTIFY_ENABLED", True)
    @patch(SIGNALS_PATH + ".DISCORDNOTIFY_SUPERUSER_ONLY", False)
    def test_should_forward_when_new_notification_is_created(
        self, mock_send_message_to_discord_user
    ):
        # given
        DiscordUser.objects.create(user=self.user, uid=123)
        # when
        notify(self.user, title="title", message="message")
        # then
        self.assertTrue(mock_send_message_to_discord_user.called)
        _, kwargs = mock_send_message_to_discord_user.call_args
        self.assertEqual(kwargs["discord_uid"], 123)
        self.assertEqual(kwargs["embed"].description, "message")
        self.assertEqual(kwargs["embed"].title, "title")

    @patch(SIGNALS_PATH + ".DISCORDNOTIFY_ENABLED", True)
    @patch(SIGNALS_PATH + ".DISCORDNOTIFY_SUPERUSER_ONLY", False)
    def test_should_split_messages_that_are_too_long(
        self, mock_send_message_to_discord_user
    ):
        # given
        DiscordUser.objects.create(user=self.user, uid=123)
        # when
        notify(self.user, title="title", message="x" * 3000)
        # then
        self.assertTrue(mock_send_message_to_discord_user.called)
        _, kwargs = mock_send_message_to_discord_user.call_args
        self.assertEqual(len(kwargs["embed"].description), 2048)

    @patch(SIGNALS_PATH + ".DISCORDNOTIFY_SUPERUSER_ONLY", False)
    def test_should_not_forward_when_app_is_disabled(
        self, mock_send_message_to_discord_user
    ):
        # given
        DiscordUser.objects.create(user=self.user, uid=123)
        # when
        with patch(SIGNALS_PATH + ".DISCORDNOTIFY_ENABLED", False):
            notify(self.user, "hi")
        # then
        self.assertFalse(mock_send_message_to_discord_user.called)

    @patch(SIGNALS_PATH + ".DISCORDNOTIFY_ENABLED", True)
    @patch(SIGNALS_PATH + ".DISCORDNOTIFY_SUPERUSER_ONLY", False)
    def test_should_not_forward_when_notification_is_updated(
        self, mock_send_message_to_discord_user
    ):
        # given
        DiscordUser.objects.create(user=self.user, uid=123)
        post_save.disconnect(forward_new_notifications, sender=Notification)
        notify(self.user, "hi")
        post_save.connect(forward_new_notifications, sender=Notification)
        # when
        notif = Notification.objects.filter(user=self.user).first()
        notif.mark_viewed()
        # then
        self.assertFalse(mock_send_message_to_discord_user.called)

    @patch(SIGNALS_PATH + ".DISCORDNOTIFY_ENABLED", True)
    @patch(SIGNALS_PATH + ".DISCORDNOTIFY_SUPERUSER_ONLY", False)
    def test_should_not_forward_when_user_has_no_account(
        self, mock_send_message_to_discord_user
    ):
        # when
        notify(self.user, "hi")
        # then
        self.assertFalse(mock_send_message_to_discord_user.called)

    @patch(SIGNALS_PATH + ".DISCORDNOTIFY_ENABLED", True)
    @patch(SIGNALS_PATH + ".DISCORDNOTIFY_SUPERUSER_ONLY", True)
    def test_should_forward_to_superusers_only_1(
        self, mock_send_message_to_discord_user
    ):
        # given
        DiscordUser.objects.create(user=self.user, uid=123)
        # when
        notify(self.user, "hi")
        # then
        self.assertFalse(mock_send_message_to_discord_user.called)

    @patch(SIGNALS_PATH + ".DISCORDNOTIFY_ENABLED", True)
    @patch(SIGNALS_PATH + ".DISCORDNOTIFY_SUPERUSER_ONLY", True)
    def test_should_forward_to_superusers_only_2(
        self, mock_send_message_to_discord_user
    ):
        # given
        user = User.objects.create_superuser("Clark Kent")
        DiscordUser.objects.create(user=user, uid=987)
        # when
        notify(user, "hi")
        # then
        self.assertTrue(mock_send_message_to_discord_user.called)

    @patch(SIGNALS_PATH + ".DISCORDNOTIFY_ENABLED", True)
    @patch(SIGNALS_PATH + ".DISCORDNOTIFY_SUPERUSER_ONLY", True)
    def test_should_forward_to_superusers_only_3(
        self, mock_send_message_to_discord_user
    ):
        # given
        user = User.objects.create_superuser("Clark Kent")
        DiscordUser.objects.create(user=user, uid=987)
        post_save.disconnect(forward_new_notifications, sender=Notification)
        notify(user, "hi")
        post_save.connect(forward_new_notifications, sender=Notification)
        # when
        notif = Notification.objects.filter(user=user).first()
        notif.mark_viewed()
        # then
        self.assertFalse(mock_send_message_to_discord_user.called)

    @patch(CORE_PATH + ".DISCORDNOTIFY_MARK_AS_VIEWED", True)
    @patch(SIGNALS_PATH + ".DISCORDNOTIFY_ENABLED", True)
    @patch(SIGNALS_PATH + ".DISCORDNOTIFY_SUPERUSER_ONLY", False)
    def test_should_mark_notification_as_viewed_once_submitted(
        self, mock_send_message_to_discord_user
    ):
        # given
        DiscordUser.objects.create(user=self.user, uid=123)
        # when
        obj = Notification.objects.notify_user(user=self.user, title="hi")
        # then
        obj.refresh_from_db()
        self.assertTrue(obj.viewed)

    @patch(CORE_PATH + ".DISCORDNOTIFY_MARK_AS_VIEWED", False)
    @patch(SIGNALS_PATH + ".DISCORDNOTIFY_ENABLED", True)
    @patch(SIGNALS_PATH + ".DISCORDNOTIFY_SUPERUSER_ONLY", False)
    def test_should_not_mark_notification_as_viewed_once_submitted(
        self, mock_send_message_to_discord_user
    ):
        # given
        DiscordUser.objects.create(user=self.user, uid=123)
        # when
        obj = Notification.objects.notify_user(user=self.user, title="hi")
        # then
        obj.refresh_from_db()
        self.assertFalse(obj.viewed)

    @patch(CORE_PATH + ".DISCORDNOTIFY_MARK_AS_VIEWED", False)
    @patch(SIGNALS_PATH + ".DISCORDNOTIFY_ENABLED", True)
    @patch(SIGNALS_PATH + ".DISCORDNOTIFY_SUPERUSER_ONLY", False)
    def test_should_not_mark_notification_as_viewed_when_failed(
        self, mock_send_message_to_discord_user
    ):
        # given
        mock_send_message_to_discord_user.side_effect = OSError
        DiscordUser.objects.create(user=self.user, uid=123)
        # when
        obj = Notification.objects.notify_user(user=self.user, title="hi")
        # then
        obj.refresh_from_db()
        self.assertFalse(obj.viewed)


class TestViews(TestCase):
    @patch(VIEWS_PATH + ".notify", wraps=notify)
    @patch(VIEWS_PATH + ".messages_plus")
    def test_should_create_notification_and_send_message(
        self, spy_messages_plus, spy_notify
    ):
        # given
        user = User.objects.create_user("Bruce Wayne")
        factory = RequestFactory()
        request = factory.get(reverse("discordnotify:send_test_notification"))
        request.user = user
        # when
        response = views.send_test_notification(request)
        # then
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("authentication:dashboard"))
        self.assertTrue(spy_notify.called)
        self.assertTrue(spy_messages_plus.success.called)
