from django.contrib import admin
from .models import Investor, InvestorPortfolio, Investment

@admin.register(Investor)
class InvestorAdmin(admin.ModelAdmin):
    list_display = ['user', 'investor_type', 'accredited', 'institution']

@admin.register(InvestorPortfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ['investor', 'total_invested', 'current_value', 'irr', 'default_rate']

@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ['portfolio', 'loan', 'amount_invested', 'share_percentage', 'status']
