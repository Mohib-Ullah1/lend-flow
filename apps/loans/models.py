from django.db import models
from apps.core.models import TenantModel

class LoanProduct(TenantModel):
    PRODUCT_TYPES = [('personal','Personal'),('business','Business'),('auto','Auto'),('mortgage','Mortgage'),('line_of_credit','Line of Credit'),('bnpl','Buy Now Pay Later')]
    REPAYMENT_TYPES = [('emi','EMI'),('bullet','Bullet'),('balloon','Balloon'),('interest_only','Interest Only')]

    name = models.CharField(max_length=100)
    product_type = models.CharField(max_length=30, choices=PRODUCT_TYPES)
    min_amount = models.DecimalField(max_digits=14, decimal_places=2)
    max_amount = models.DecimalField(max_digits=14, decimal_places=2)
    min_term_months = models.PositiveIntegerField()
    max_term_months = models.PositiveIntegerField()
    base_interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    rate_spread_by_grade = models.JSONField(default=dict, blank=True)
    origination_fee_pct = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    late_fee_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    late_fee_grace_days = models.PositiveIntegerField(default=5)
    repayment_type = models.CharField(max_length=20, choices=REPAYMENT_TYPES, default='emi')
    requires_collateral = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'loan_products'

    def __str__(self):
        return f'{self.name} ({self.product_type})'


class LoanApplication(TenantModel):
    STATUS_CHOICES = [('draft','Draft'),('submitted','Submitted'),('under_review','Under Review'),('approved','Approved'),('rejected','Rejected'),('disbursed','Disbursed'),('cancelled','Cancelled')]
    GRADE_CHOICES = [('A+','A+'),('A','A'),('B','B'),('C','C'),('D','D'),('E','E')]

    borrower = models.ForeignKey('borrowers.Borrower', on_delete=models.PROTECT, related_name='applications')
    product = models.ForeignKey(LoanProduct, on_delete=models.PROTECT)
    amount_requested = models.DecimalField(max_digits=14, decimal_places=2)
    amount_approved = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    term_months = models.PositiveIntegerField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    purpose = models.TextField(blank=True, default='')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    risk_grade = models.CharField(max_length=5, choices=GRADE_CHOICES, blank=True, default='')
    risk_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    risk_factors = models.JSONField(default=list, blank=True)
    approval_level = models.CharField(max_length=30, blank=True, default='')
    decision_reason = models.TextField(blank=True, default='')
    submitted_at = models.DateTimeField(null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    rejected_at = models.DateTimeField(null=True, blank=True)
    disbursed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_applications')

    class Meta:
        db_table = 'loan_applications'
        indexes = [models.Index(fields=['institution', 'status']), models.Index(fields=['borrower', 'status'])]

    def __str__(self):
        return f'APP-{str(self.id)[:8]} ({self.status})'


class Loan(TenantModel):
    STATUS_CHOICES = [('active','Active'),('paid_off','Paid Off'),('delinquent','Delinquent'),('defaulted','Defaulted'),('restructured','Restructured'),('written_off','Written Off')]

    application = models.OneToOneField(LoanApplication, on_delete=models.PROTECT, related_name='loan')
    borrower = models.ForeignKey('borrowers.Borrower', on_delete=models.PROTECT, related_name='loans')
    product = models.ForeignKey(LoanProduct, on_delete=models.PROTECT)
    principal_amount = models.DecimalField(max_digits=14, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    term_months = models.PositiveIntegerField()
    origination_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_interest = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total_payable = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    outstanding_principal = models.DecimalField(max_digits=14, decimal_places=2)
    outstanding_interest = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    outstanding_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    disbursement_date = models.DateField()
    first_payment_date = models.DateField()
    maturity_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    days_past_due = models.PositiveIntegerField(default=0)
    last_payment_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'loans'
        indexes = [models.Index(fields=['institution', 'status']), models.Index(fields=['borrower', 'status'])]

    def __str__(self):
        return f'LN-{str(self.id)[:8]} ({self.status})'
