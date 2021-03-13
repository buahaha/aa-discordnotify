from app_utils.logging import LoggerAddTag

from django.core.exceptions import ObjectDoesNotExist
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
    if created and (not DISCORDNOTIFY_SUPERUSER_ONLY or instance.user.is_superuser):
        logger.info("Processing notification %d for: %s", instance.id, instance.user)
        try:
            discord_uid = instance.user.discord.uid
        except ObjectDoesNotExist:
            logger.info(
                "Can not forward notification to user %s, because he has no Discord account",
                instance.user,
            )
            return
        # we are passing through the instance attributes, because it is not garanteed
        # that the object has already been saved
        task_forward_notification_to_discord.delay(
            notification_id=instance.id,
            discord_uid=discord_uid,
            title=instance.title,
            message=instance.message,
            level=instance.level,
            timestamp=instance.timestamp.isoformat(),
        )
    else:
        logger.info(
            "Ignoring notification %d for: %s", instance.id, instance.user
        )  # TODO: set back to debug for stable release
