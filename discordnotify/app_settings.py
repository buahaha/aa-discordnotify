from django.conf import settings

# Port used to communicate with Discord Proxy
DISCORDNOTIFY_DISCORDPROXY_PORT = getattr(
    settings, "DISCORDNOTIFY_DISCORDPROXY_PORT", 50051
)

# When set to True, only superusers will be get their notifications forwarded
DISCORDNOTIFY_SUPERUSER_ONLY = getattr(settings, "DISCORDNOTIFY_SUPERUSER_ONLY", False)
