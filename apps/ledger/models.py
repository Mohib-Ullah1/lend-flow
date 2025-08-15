from django.db import models
from apps.core.models import TimeStampedModel

class GLAccount(TimeStampedModel):
    TYPE_CHOICES = [('asset','Asset'),('liability','Liability'),('equity','Equity'),('revenue','Revenue'),('expense','Expense')]

    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    account_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'gl_accounts'
        ordering = ['code']

    def __str__(self):
        return f'{self.code} {self.name}'


class JournalEntry(TimeStampedModel):
    institution = models.ForeignKey('institutions.Institution', on_delete=models.CASCADE)
    reference_type = models.CharField(max_length=50)
    reference_id = models.UUIDField()
    description = models.TextField()
    entry_date = models.DateField()
    is_reversed = models.BooleanField(default=False)

    class Meta:
        db_table = 'journal_entries'
        verbose_name_plural = 'journal entries'

    def __str__(self):
        return f'JE-{self.entry_date} {self.description[:50]}'


class JournalLine(models.Model):
    id = models.BigAutoField(primary_key=True)
    entry = models.ForeignKey(JournalEntry, on_delete=models.CASCADE, related_name='lines')
    account = models.ForeignKey(GLAccount, on_delete=models.PROTECT)
    debit = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    class Meta:
        db_table = 'journal_lines'

    def __str__(self):
        return f'{self.account.code}: DR {self.debit} / CR {self.credit}'
