from decimal import Decimal, ROUND_HALF_UP
from dateutil.relativedelta import relativedelta

def generate_schedule(loan):
    from .models import RepaymentSchedule

    principal = Decimal(str(loan.principal_amount))
    rate = Decimal(str(loan.interest_rate))
    term = loan.term_months
    monthly_rate = rate / Decimal('1200')
    start_date = loan.first_payment_date

    if monthly_rate > 0:
        r = monthly_rate
        n = term
        emi = principal * (r * (1 + r) ** n) / ((1 + r) ** n - 1)
    else:
        emi = principal / term

    emi = Decimal(str(emi)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    remaining = principal
    entries = []

    for i in range(1, term + 1):
        interest = (remaining * monthly_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        principal_part = emi - interest
        if i == term:
            principal_part = remaining
            emi = principal_part + interest
        remaining -= principal_part
        due_date = start_date + relativedelta(months=i - 1)

        entries.append(RepaymentSchedule(
            loan=loan,
            installment_number=i,
            due_date=due_date,
            amount_due=emi,
            principal_component=principal_part,
            interest_component=interest,
        ))

    RepaymentSchedule.objects.bulk_create(entries)
