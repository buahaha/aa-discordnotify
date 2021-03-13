from app_utils.logging import LoggerAddTag
from celery import shared_task

from allianceauth.notifications.models import Notification
from allianceauth.services.hooks import get_extension_logger

from . import __title__
from .core import forward_notification_to_discord

logger = LoggerAddTag(get_extension_logger(__name__), __title__)


@shared_task
def task_forward_notification_to_discord(notification_id):
    logger.info("Started task to forward notification %d", notification_id)
    notification = Notification.objects.get(id=notification_id)
    forward_notification_to_discord(notification)
