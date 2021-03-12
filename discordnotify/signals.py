from django.db.models.signals import post_save
from django.dispatch import receiver

from allianceauth.notifications.models import Notification
from allianceauth.services.hooks import get_extension_logger

from app_utils.logging import LoggerAddTag

from . import __title__
from .tasks import forward_notification_to_discord_user


logger = LoggerAddTag(get_extension_logger(__name__), __title__)


@receiver(post_save, sender=Notification)
def my_handler(instance, created, **kwargs):
    if created:
        logger.info("Processing new notification for: %s", instance.user)
        forward_notification_to_discord_user.delay(instance.id)
