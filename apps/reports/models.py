from django.db import models
from apps.core.models import TenantModel

class Report(TenantModel):
    FORMAT_CHOICES = [('pdf','PDF'),('csv','CSV'),('excel','Excel')]
    STATUS_CHOICES = [('pending','Pending'),('generating','Generating'),('completed','Completed'),('failed','Failed')]

    name = models.CharField(max_length=255)
    report_type = models.CharField(max_length=50)  # portfolio_summary, collections, financial, pipeline, investor, compliance
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default='pdf')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    parameters = models.JSONField(default=dict, blank=True)
    file = models.FileField(upload_to='reports/%Y/%m/', null=True, blank=True)
    file_size = models.PositiveIntegerField(default=0)
    generated_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True)
    generated_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True, default='')

    class Meta:
        db_table = 'reports'

    def __str__(self):
        return f'{self.name} ({self.status})'
