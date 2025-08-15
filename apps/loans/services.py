from decimal import Decimal
from datetime import date
from dateutil.relativedelta import relativedelta


def disburse_loan(application):
    from .models import Loan

    principal = application.amount_approved or application.amount_requested
    rate = application.interest_rate
    term = application.term_months
    monthly_rate = rate / 12 / 100

    if monthly_rate > 0:
        emi = principal * (monthly_rate * (1 + monthly_rate) ** term) / ((1 + monthly_rate) ** term - 1)
    else:
        emi = principal / term

    total_payable = emi * term
    total_interest = total_payable - principal
    origination_fee = principal * (application.product.origination_fee_pct / 100)

    today = date.today()
    first_payment = today + relativedelta(months=1)
    maturity = today + relativedelta(months=term)

    loan = Loan.objects.create(
        institution=application.institution,
        application=application,
        borrower=application.borrower,
        product=application.product,
        principal_amount=principal,
        interest_rate=rate,
        term_months=term,
        origination_fee=origination_fee,
        total_interest=round(total_interest, 2),
        total_payable=round(total_payable, 2),
        outstanding_principal=principal,
        disbursement_date=today,
        first_payment_date=first_payment,
        maturity_date=maturity,
    )

    # Generate repayment schedule
    from apps.repayments.services import generate_schedule
    generate_schedule(loan)

    return loan
