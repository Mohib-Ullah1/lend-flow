from django.contrib import admin
from .models import KYCVerification

@admin.register(KYCVerification)
class KYCVerificationAdmin(admin.ModelAdmin):
    list_display = ['borrower', 'verification_type', 'status', 'verified_at']
    list_filter = ['verification_type', 'status']
