import json, hashlib
from django.db import models

class AuditLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    institution_id = models.UUIDField(null=True, blank=True, db_index=True)
    user_id = models.UUIDField(null=True, blank=True)
    username = models.CharField(max_length=150, blank=True, default='')
    action = models.CharField(max_length=50)
    resource_type = models.CharField(max_length=50)
    resource_id = models.CharField(max_length=100, blank=True, default='')
    changes = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, default='')
    integrity_hash = models.CharField(max_length=64, blank=True, default='')

    class Meta:
        db_table = 'audit_logs'
        ordering = ['-timestamp']

    def save(self, *args, **kwargs):
        if not self.integrity_hash:
            payload = json.dumps({
                'action': self.action, 'resource_type': self.resource_type,
                'resource_id': self.resource_id, 'changes': self.changes,
            }, sort_keys=True)
            self.integrity_hash = hashlib.sha256(payload.encode()).hexdigest()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.action} {self.resource_type} by {self.username}'
