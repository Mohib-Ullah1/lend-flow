from django.db import models
from apps.core.models import TimeStampedModel

class Notification(TimeStampedModel):
    TYPE_CHOICES = [('email','Email'),('sms','SMS'),('in_app','In-App'),('push','Push')]

    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='in_app')
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    action_url = models.CharField(max_length=500, blank=True, default='')
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'notifications'

    def __str__(self):
        return f'{self.title} ({self.notification_type})'
