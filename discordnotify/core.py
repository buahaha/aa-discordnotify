import grpc
from app_utils.logging import LoggerAddTag
from app_utils.urls import reverse_absolute, static_file_absolute_url
from discordproxy.discord_api_pb2 import Embed, SendDirectMessageRequest
from discordproxy.discord_api_pb2_grpc import DiscordApiStub

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from allianceauth.notifications.models import Notification
from allianceauth.services.hooks import get_extension_logger

from . import __title__

logger = LoggerAddTag(get_extension_logger(__name__), __title__)

# embed colors
COLOR_INFO = 0x5BC0DE
COLOR_SUCCESS = 0x5CB85C
COLOR_WARNING = 0xF0AD4E
COLOR_DANGER = 0xD9534F

COLOR_MAP = {
    "info": COLOR_INFO,
    "success": COLOR_SUCCESS,
    "warning": COLOR_WARNING,
    "danger": COLOR_DANGER,
}


def forward_notification_to_discord(notification: Notification):
    try:
        discord_user_id = notification.user.discord.uid
    except ObjectDoesNotExist:
        logger.info(
            "Can not forward notification to user %s, because he has no Discord account",
            notification.user,
        )
        return
    embed = Embed(
        author=Embed.Author(
            name="Alliance Auth Notification",
            icon_url=static_file_absolute_url("icons/apple-touch-icon.png"),
        ),
        title=notification.title,
        url=reverse_absolute("notifications:list"),
        description=notification.message,
        color=COLOR_MAP.get(notification.level, None),
        timestamp=notification.timestamp.isoformat(),
        footer=Embed.Footer(text=settings.SITE_NAME),
    )
    logger.info("Forwarding notification to %s", notification.user)
    _send_message_to_discord_user(user_id=discord_user_id, embed=embed)


def _send_message_to_discord_user(user_id, embed):
    with grpc.insecure_channel("localhost:50051") as channel:
        client = DiscordApiStub(channel)
        request = SendDirectMessageRequest(user_id=user_id, embed=embed)
        client.SendDirectMessage(request)
