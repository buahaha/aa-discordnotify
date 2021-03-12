from unittest.mock import patch

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.test import TestCase, override_settings

from allianceauth.notifications import notify
from allianceauth.notifications.models import Notification
from allianceauth.services.modules.discord.models import DiscordUser

from .signals import forward_new_notifications

SIGNALS_PATH = "discordnotify.signals"
CORE_PATH = "discordnotify.core"


@patch(CORE_PATH + "._send_message_to_discord_user")
@override_settings(CELERY_ALWAYS_EAGER=True)
class TestIntegration(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create_user("Bruce Wayne")

    @patch(SIGNALS_PATH + ".DISCORDNOTIFY_SUPERUSER_ONLY", False)
    def test_should_forward_when_new_notification_is_created(
        self, mock_send_message_to_discord_user
    ):
        # given
        DiscordUser.objects.create(user=self.user, uid=123)
        # when
        notify(self.user, "hi")
        # then
        self.assertTrue(mock_send_message_to_discord_user.called)

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

    @patch(SIGNALS_PATH + ".DISCORDNOTIFY_SUPERUSER_ONLY", False)
    def test_should_not_forward_when_user_has_no_account(
        self, mock_send_message_to_discord_user
    ):
        # when
        notify(self.user, "hi")
        # then
        self.assertFalse(mock_send_message_to_discord_user.called)

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
