from django.contrib import admin
from .models import LoanProduct, LoanApplication, Loan

@admin.register(LoanProduct)
class LoanProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'product_type', 'base_interest_rate', 'min_amount', 'max_amount', 'is_active', 'institution']
    list_filter = ['product_type', 'is_active', 'institution']

@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'borrower', 'amount_requested', 'status', 'risk_grade', 'submitted_at']
    list_filter = ['status', 'risk_grade', 'institution']
    search_fields = ['borrower__email']

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'borrower', 'principal_amount', 'outstanding_principal', 'status', 'days_past_due']
    list_filter = ['status', 'institution']
