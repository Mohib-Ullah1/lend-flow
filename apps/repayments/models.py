from django.db import models
from apps.core.models import TimeStampedModel

class RepaymentSchedule(TimeStampedModel):
    STATUS_CHOICES = [('scheduled','Scheduled'),('pending','Pending'),('paid','Paid'),('partially_paid','Partially Paid'),('overdue','Overdue'),('waived','Waived')]

    loan = models.ForeignKey('loans.Loan', on_delete=models.CASCADE, related_name='schedule')
    installment_number = models.PositiveIntegerField()
    due_date = models.DateField()
    amount_due = models.DecimalField(max_digits=14, decimal_places=2)
    principal_component = models.DecimalField(max_digits=14, decimal_places=2)
    interest_component = models.DecimalField(max_digits=14, decimal_places=2)
    fee_component = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount_paid = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    paid_at = models.DateTimeField(null=True, blank=True)
    days_overdue = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'repayment_schedules'
        ordering = ['loan', 'installment_number']
        constraints = [models.UniqueConstraint(fields=['loan', 'installment_number'], name='unique_installment')]

    def __str__(self):
        return f'#{self.installment_number} - {self.due_date} ({self.status})'


class Payment(TimeStampedModel):
    STATUS_CHOICES = [('pending','Pending'),('completed','Completed'),('failed','Failed'),('reversed','Reversed')]

    loan = models.ForeignKey('loans.Loan', on_delete=models.PROTECT, related_name='payments')
    installment = models.ForeignKey(RepaymentSchedule, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    payment_method = models.CharField(max_length=30, default='ach')
    payment_reference = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    processed_at = models.DateTimeField(null=True, blank=True)
    failure_reason = models.TextField(blank=True, default='')

    class Meta:
        db_table = 'payments'

    def __str__(self):
        return f'PAY-{str(self.id)[:6]} ${self.amount}'
