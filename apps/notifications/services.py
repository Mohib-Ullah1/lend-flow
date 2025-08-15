from django.core.mail import send_mail
from django.conf import settings

def send_email_notification(user, subject, message):
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=True)
        return True
    except Exception:
        return False

def create_notification(user, title, message, notification_type='in_app', action_url='', metadata=None):
    from .models import Notification
    return Notification.objects.create(
        user=user,
        notification_type=notification_type,
        title=title,
        message=message,
        action_url=action_url,
        metadata=metadata or {},
    )

def notify_application_status(application, new_status):
    """Send notification when application status changes."""
    user = application.borrower.user
    if not user:
        return

    status_messages = {
        'approved': ('Application Approved!', f'Your loan application for ${application.amount_requested} has been approved.'),
        'rejected': ('Application Update', f'Your loan application for ${application.amount_requested} was not approved.'),
        'disbursed': ('Funds Disbursed!', f'${application.amount_approved or application.amount_requested} has been sent to your account.'),
    }

    if new_status in status_messages:
        title, message = status_messages[new_status]
        create_notification(user, title, message, action_url=f'/applications/{application.id}/')
        send_email_notification(user, title, message)
