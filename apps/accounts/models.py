import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('super_admin', 'Super Admin'),
        ('institution_admin', 'Institution Admin'),
        ('senior_underwriter', 'Senior Underwriter'),
        ('junior_underwriter', 'Junior Underwriter'),
        ('collections_agent', 'Collections Agent'),
        ('analyst', 'Analyst'),
        ('borrower', 'Borrower'),
        ('investor', 'Investor'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    institution = models.ForeignKey(
        'institutions.Institution',
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='users',
    )
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='borrower')
    phone = models.CharField(max_length=20, blank=True, default='')
    mfa_enabled = models.BooleanField(default=False)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f'{self.get_full_name()} ({self.role})'
