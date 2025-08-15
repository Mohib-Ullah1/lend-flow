from django.db import models
from apps.core.models import TenantModel

class Borrower(TenantModel):
    KYC_CHOICES = [('pending','Pending'),('in_progress','In Progress'),('verified','Verified'),('rejected','Rejected')]

    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, null=True, blank=True, related_name='borrower_profile')
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    kyc_status = models.CharField(max_length=20, choices=KYC_CHOICES, default='pending')
    risk_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    risk_grade = models.CharField(max_length=5, blank=True, default='')
    is_blacklisted = models.BooleanField(default=False)

    class Meta:
        db_table = 'borrowers'
        constraints = [models.UniqueConstraint(fields=['institution', 'email'], name='unique_borrower_email_per_inst')]

    def __str__(self):
        return f'{self.email} ({self.kyc_status})'


class BorrowerProfile(models.Model):
    borrower = models.OneToOneField(Borrower, on_delete=models.CASCADE, primary_key=True, related_name='profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    ssn_last4 = models.CharField(max_length=4, blank=True, default='')
    address = models.JSONField(default=dict, blank=True)
    employment_status = models.CharField(max_length=30, blank=True, default='')
    employer_name = models.CharField(max_length=255, blank=True, default='')
    job_title = models.CharField(max_length=255, blank=True, default='')
    annual_income = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    monthly_expenses = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    income_verified = models.BooleanField(default=False)

    class Meta:
        db_table = 'borrower_profiles'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
