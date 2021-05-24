from math import ceil

import grpc
from discordproxy.discord_api_pb2 import Embed, SendDirectMessageRequest
from discordproxy.discord_api_pb2_grpc import DiscordApiStub

from django.conf import settings

from allianceauth.notifications.models import Notification
from allianceauth.services.hooks import get_extension_logger
from app_utils.logging import LoggerAddTag
from app_utils.urls import reverse_absolute, static_file_absolute_url

from . import __title__
from .app_settings import DISCORDNOTIFY_DISCORDPROXY_PORT, DISCORDNOTIFY_MARK_AS_VIEWED

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

# limits
MAX_LENGTH_TITLE = 256
MAX_LENGTH_DESCRIPTION = 2048


def forward_notification_to_discord(
    notification_id: int,
    discord_uid: int,
    title: str,
    message: str,
    level: str,
    timestamp: str,
):
    message_trimmed = message.strip()
    message_count = ceil(len(message_trimmed) / MAX_LENGTH_DESCRIPTION)
    for n in range(message_count):
        logger.info("Forwarding notification %d to %s", notification_id, discord_uid)
        title_embed = title.strip()
        if message_count > 1:
            title_embed += f" ({n + 1}/{message_count})"
        embed = Embed(
            author=Embed.Author(
                name="Alliance Auth Notification",
                icon_url=static_file_absolute_url("icons/apple-touch-icon.png"),
            ),
            title=title_embed[:MAX_LENGTH_TITLE],
            url=reverse_absolute("notifications:view", args=[notification_id]),
            description=message[
                n * MAX_LENGTH_DESCRIPTION : (n + 1) * MAX_LENGTH_DESCRIPTION
            ],
            color=COLOR_MAP.get(level, None),
            timestamp=timestamp,
            footer=Embed.Footer(text=settings.SITE_NAME),
        )
        _send_message_to_discord_user(discord_uid=discord_uid, embed=embed)
    _mark_as_viewed(notification_id)


def _send_message_to_discord_user(discord_uid: int, embed: Embed):
    with grpc.insecure_channel(
        f"localhost:{DISCORDNOTIFY_DISCORDPROXY_PORT}"
    ) as channel:
        client = DiscordApiStub(channel)
        request = SendDirectMessageRequest(user_id=discord_uid, embed=embed)
        try:
            client.SendDirectMessage(request)
        except grpc.RpcError as e:
            logger.error(
                "Failed to send message to Discord API: %s: %s",
                e.code(),
                e.details(),
            )


def _mark_as_viewed(notification_id):
    if DISCORDNOTIFY_MARK_AS_VIEWED:
        try:
            notif = Notification.objects.get(id=notification_id)
        except Notification.DoesNotExist:
            return
        else:
            notif.mark_viewed()
