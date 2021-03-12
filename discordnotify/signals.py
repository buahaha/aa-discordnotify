from app_utils.logging import LoggerAddTag

from django.db.models.signals import post_save
from django.dispatch import receiver

from allianceauth.notifications.models import Notification
from allianceauth.services.hooks import get_extension_logger

from . import __title__
from .app_settings import DISCORDNOTIFY_SUPERUSER_ONLY
from .tasks import task_forward_notification_to_discord

logger = LoggerAddTag(get_extension_logger(__name__), __title__)


@receiver(post_save, sender=Notification)
def forward_new_notifications(instance, created, **kwargs):
    if created and not DISCORDNOTIFY_SUPERUSER_ONLY or instance.user.is_superuser:
        logger.info("Processing new notification for: %s", instance.user)
        task_forward_notification_to_discord.delay(instance.id)
