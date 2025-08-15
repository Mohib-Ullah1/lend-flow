from django.contrib import admin
from .models import RepaymentSchedule, Payment

@admin.register(RepaymentSchedule)
class RepaymentScheduleAdmin(admin.ModelAdmin):
    list_display = ['loan', 'installment_number', 'due_date', 'amount_due', 'amount_paid', 'status']
    list_filter = ['status']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_reference', 'loan', 'amount', 'payment_method', 'status', 'processed_at']
    list_filter = ['status', 'payment_method']
