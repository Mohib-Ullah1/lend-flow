from django.db import models
from apps.core.models import TenantModel

class Investor(TenantModel):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, related_name='investor_profile')
    investor_type = models.CharField(max_length=30, default='individual')
    accredited = models.BooleanField(default=False)
    investment_preferences = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'investors'

    def __str__(self):
        return f'{self.user.get_full_name()} ({self.investor_type})'


class InvestorPortfolio(TenantModel):
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE, related_name='portfolios')
    name = models.CharField(max_length=100, default='Default Portfolio')
    total_invested = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    current_value = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total_returns = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    irr = models.DecimalField(max_digits=7, decimal_places=4, null=True, blank=True)
    par_30 = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    par_60 = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    par_90 = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    default_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    class Meta:
        db_table = 'investor_portfolios'

    def __str__(self):
        return f'{self.investor} — {self.name}'


class Investment(TenantModel):
    portfolio = models.ForeignKey(InvestorPortfolio, on_delete=models.CASCADE, related_name='investments')
    loan = models.ForeignKey('loans.Loan', on_delete=models.PROTECT, related_name='investments')
    amount_invested = models.DecimalField(max_digits=14, decimal_places=2)
    share_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=20, default='active')

    class Meta:
        db_table = 'investments'
        constraints = [models.UniqueConstraint(fields=['portfolio', 'loan'], name='unique_portfolio_loan')]

    def __str__(self):
        return f'{self.portfolio.investor} -> {self.loan} ({self.share_percentage}%)'
