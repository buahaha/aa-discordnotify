from app_utils.logging import LoggerAddTag
from celery import shared_task

from allianceauth.services.hooks import get_extension_logger

from . import __title__
from .core import forward_notification_to_discord

logger = LoggerAddTag(get_extension_logger(__name__), __title__)


@shared_task
def task_forward_notification_to_discord(
    notification_id: int,
    discord_uid: int,
    title: str,
    message: str,
    level: str,
    timestamp: str,
):
    logger.info("Started task to forward notification %d", notification_id)
    forward_notification_to_discord(
        notification_id=notification_id,
        discord_uid=discord_uid,
        title=title,
        message=message,
        level=level,
        timestamp=timestamp,
    )
