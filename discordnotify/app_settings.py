from django.conf import settings


# When set to True, only superusers will be get their notifications forwarded
DISCORDNOTIFY_SUPERUSER_ONLY = getattr(settings, "DISCORDNOTIFY_SUPERUSER_ONLY", False)
