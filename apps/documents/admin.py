from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['original_filename', 'document_type', 'borrower', 'verification_status', 'file_size', 'created_at']
    list_filter = ['document_type', 'verification_status']
