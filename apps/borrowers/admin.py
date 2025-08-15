from django.contrib import admin
from .models import Borrower, BorrowerProfile

class BorrowerProfileInline(admin.StackedInline):
    model = BorrowerProfile
    can_delete = False

@admin.register(Borrower)
class BorrowerAdmin(admin.ModelAdmin):
    list_display = ['email', 'phone', 'kyc_status', 'risk_grade', 'institution', 'created_at']
    list_filter = ['kyc_status', 'risk_grade', 'is_blacklisted', 'institution']
    search_fields = ['email', 'phone', 'profile__first_name', 'profile__last_name']
    inlines = [BorrowerProfileInline]
