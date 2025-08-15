from apps.core.models import TimeStampedModel
import uuid
from django.db import models

class Institution(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    branding = models.JSONField(default=dict, blank=True)
    custom_domain = models.CharField(max_length=255, blank=True, default='')
    product_config = models.JSONField(default=dict, blank=True)
    workflow_config = models.JSONField(default=dict, blank=True)
    scoring_config = models.JSONField(default=dict, blank=True)
    dunning_config = models.JSONField(default=dict, blank=True)
    regulatory_region = models.CharField(max_length=50, default='US')
    api_key_hash = models.CharField(max_length=255, blank=True, default='')
    webhook_url = models.URLField(blank=True, default='')
    max_loan_amount = models.DecimalField(max_digits=14, decimal_places=2, default=500000)
    support_email = models.EmailField(blank=True, default='')

    class Meta:
        db_table = 'institutions'

    def __str__(self):
        return self.name
