from app_utils.messages import messages_plus

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from allianceauth.notifications import notify


@login_required
def send_test_notification(request):
    notify(
        request.user,
        title="Test Notification",
        message=f"This is a test notification from Discord Notify created for {request.user}.",
    )
    messages_plus.success(
        request, f"Discord Notify: Test notification was created for {request.user}"
    )
    return redirect("authentication:dashboard")
