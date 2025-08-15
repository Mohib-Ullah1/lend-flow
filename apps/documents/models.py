import hashlib
from django.db import models
from apps.core.models import TenantModel

class Document(TenantModel):
    STATUS_CHOICES = [('pending','Pending'),('verified','Verified'),('rejected','Rejected')]

    borrower = models.ForeignKey('borrowers.Borrower', on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=50)  # government_id, proof_of_address, income_proof, loan_agreement
    file = models.FileField(upload_to='documents/%Y/%m/')
    original_filename = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField(default=0)
    file_hash = models.CharField(max_length=64, blank=True, default='')
    verification_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    verified_by = models.CharField(max_length=100, blank=True, default='')
    notes = models.TextField(blank=True, default='')

    class Meta:
        db_table = 'documents'

    def __str__(self):
        return f'{self.original_filename} ({self.document_type})'
