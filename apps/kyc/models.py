from django.db import models
from apps.core.models import TimeStampedModel

class KYCVerification(TimeStampedModel):
    STATUS_CHOICES = [('pending','Pending'),('in_progress','In Progress'),('passed','Passed'),('failed','Failed')]

    borrower = models.ForeignKey('borrowers.Borrower', on_delete=models.CASCADE, related_name='kyc_checks')
    verification_type = models.CharField(max_length=50)  # identity, address, income, sanctions
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    result_data = models.JSONField(default=dict, blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, default='')

    class Meta:
        db_table = 'kyc_verifications'

    def __str__(self):
        return f'{self.borrower} — {self.verification_type} ({self.status})'
