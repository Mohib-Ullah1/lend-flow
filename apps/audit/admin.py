from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'username', 'action', 'resource_type', 'resource_id', 'ip_address']
    list_filter = ['action', 'resource_type']
    search_fields = ['username', 'resource_id']
    readonly_fields = ['integrity_hash']
