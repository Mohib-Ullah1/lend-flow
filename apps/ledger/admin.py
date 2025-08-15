from django.contrib import admin
from .models import GLAccount, JournalEntry, JournalLine

@admin.register(GLAccount)
class GLAccountAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'account_type', 'is_active']
    list_filter = ['account_type', 'is_active']

class JournalLineInline(admin.TabularInline):
    model = JournalLine
    extra = 0

@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'reference_type', 'entry_date', 'institution']
    list_filter = ['reference_type', 'entry_date']
    inlines = [JournalLineInline]
