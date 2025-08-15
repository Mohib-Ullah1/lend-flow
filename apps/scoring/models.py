from django.db import models
from apps.core.models import TimeStampedModel

class CreditScore(TimeStampedModel):
    borrower = models.ForeignKey('borrowers.Borrower', on_delete=models.CASCADE, related_name='credit_scores')
    application = models.ForeignKey('loans.LoanApplication', on_delete=models.SET_NULL, null=True, blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=5)
    confidence = models.FloatField(default=0.0)
    factors = models.JSONField(default=list)
    bureau_score = models.IntegerField(null=True, blank=True)
    dti_ratio = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    auto_approve = models.BooleanField(default=False)
    scored_by = models.CharField(max_length=50, default='system')

    class Meta:
        db_table = 'credit_scores'

    def __str__(self):
        return f'{self.borrower} — {self.score} ({self.grade})'
