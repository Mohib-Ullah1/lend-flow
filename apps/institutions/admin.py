from django.contrib import admin
from .models import Institution

@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'regulatory_region', 'created_at']
    list_filter = ['is_active', 'regulatory_region']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
