from django.conf import settings

# Port used to communicate with Discord Proxy
DISCORDNOTIFY_DISCORDPROXY_PORT = getattr(
    settings, "DISCORDNOTIFY_DISCORDPROXY_PORT", 50051
)

# When set to True, only superusers will be get their notifications forwarded
DISCORDNOTIFY_SUPERUSER_ONLY = getattr(settings, "DISCORDNOTIFY_SUPERUSER_ONLY", False)

# Set this to False to disable this app temporarily
DISCORDNOTIFY_ENABLED = getattr(settings, "DISCORDNOTIFY_ENABLED", True)

# When set True will mark all notifications as read
# that have been successfully submitted to Discord
DISCORDNOTIFY_MARK_AS_VIEWED = getattr(settings, "DISCORDNOTIFY_MARK_AS_VIEWED", False)
