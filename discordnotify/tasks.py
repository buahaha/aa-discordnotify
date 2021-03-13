from celery import shared_task

from allianceauth.notifications.models import Notification

from .core import forward_notification_to_discord


@shared_task
def task_forward_notification_to_discord(notification_id):
    notification = Notification.objects.get(id=notification_id)
    forward_notification_to_discord(notification)
