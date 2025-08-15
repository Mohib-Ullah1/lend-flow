from django.contrib import admin
from .models import CreditScore

@admin.register(CreditScore)
class CreditScoreAdmin(admin.ModelAdmin):
    list_display = ['borrower', 'score', 'grade', 'auto_approve', 'created_at']
    list_filter = ['grade', 'auto_approve']
