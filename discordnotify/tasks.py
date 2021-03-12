from celery import shared_task

from allianceauth.notifications.models import Notification
from allianceauth.services.tasks import QueueOnce

from .core import forward_notification_to_discord


@shared_task(base=QueueOnce)  # using once to counter possible multi triggering
def task_forward_notification_to_discord(notification_id):
    notification = Notification.objects.get(id=notification_id)
    forward_notification_to_discord(notification)
