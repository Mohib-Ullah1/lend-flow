"""Seed demo data for LendFlow."""
import os, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()

from django.contrib.auth import get_user_model
from apps.institutions.models import Institution
from apps.borrowers.models import Borrower, BorrowerProfile
from apps.loans.models import LoanProduct, LoanApplication
from apps.ledger.models import GLAccount
from datetime import date
from decimal import Decimal

User = get_user_model()

# Institution
inst, _ = Institution.objects.get_or_create(
    slug='first-national',
    defaults={
        'name': 'First National Bank',
        'branding': {'colors': {'500': '#444ce7', '600': '#3538cd'}, 'name': 'First National Bank'},
        'workflow_config': {
            'approval_rules': [
                {'grades': ['A+', 'A'], 'max_amount': 50000, 'approval_level': 'auto'},
                {'grades': ['A+', 'A'], 'max_amount': 250000, 'approval_level': 'junior_underwriter'},
                {'grades': ['B', 'C'], 'max_amount': 100000, 'approval_level': 'junior_underwriter'},
                {'grades': ['B', 'C'], 'max_amount': 250000, 'approval_level': 'senior_underwriter'},
            ]
        },
        'regulatory_region': 'US',
        'support_email': 'support@firstnational.com',
    }
)
print(f'Institution: {inst.name}')

# Link admin to institution
admin = User.objects.get(username='admin')
admin.institution = inst
admin.save()

# Create staff users
for name, role in [('Jane Smith', 'senior_underwriter'), ('Mike Rodriguez', 'junior_underwriter'), ('Sarah Lee', 'collections_agent')]:
    first, last = name.split()
    u, created = User.objects.get_or_create(
        username=first.lower(),
        defaults={'email': f'{first.lower()}@lendflow.com', 'first_name': first, 'last_name': last, 'role': role, 'institution': inst}
    )
    if created:
        u.set_password('staff12345')
        u.save()
        print(f'  Staff: {name} ({role})')

# Loan Products
products_data = [
    {'name': 'Personal Loan', 'product_type': 'personal', 'min_amount': 1000, 'max_amount': 100000, 'min_term_months': 12, 'max_term_months': 60, 'base_interest_rate': 8.5, 'origination_fee_pct': 1.0, 'late_fee_amount': 25},
    {'name': 'Auto Loan', 'product_type': 'auto', 'min_amount': 5000, 'max_amount': 75000, 'min_term_months': 24, 'max_term_months': 72, 'base_interest_rate': 6.2, 'origination_fee_pct': 0.5, 'late_fee_amount': 35, 'requires_collateral': True},
    {'name': 'Business Loan', 'product_type': 'business', 'min_amount': 10000, 'max_amount': 500000, 'min_term_months': 12, 'max_term_months': 84, 'base_interest_rate': 4.5, 'origination_fee_pct': 1.5, 'late_fee_amount': 50},
]
products = {}
for pd in products_data:
    p, _ = LoanProduct.objects.get_or_create(institution=inst, name=pd['name'], defaults=pd)
    products[pd['product_type']] = p
    print(f'  Product: {p.name}')

# Borrowers
borrowers_data = [
    {'email': 'john@example.com', 'phone': '+1-555-123-4567', 'first_name': 'John', 'last_name': 'Doe', 'dob': '1990-01-15', 'employment': 'full_time', 'employer': 'Acme Corp', 'income': 95000, 'expenses': 3500, 'kyc': 'verified', 'score': 742, 'grade': 'A'},
    {'email': 'sarah@corp.com', 'phone': '+1-555-987-6543', 'first_name': 'Sarah', 'last_name': 'Kim', 'dob': '1985-06-20', 'employment': 'self_employed', 'employer': "Kim's Consulting", 'income': 145000, 'expenses': 5200, 'kyc': 'verified', 'score': 685, 'grade': 'B'},
    {'email': 'mike@email.com', 'phone': '+1-555-456-7890', 'first_name': 'Mike', 'last_name': 'Chen', 'dob': '1992-11-08', 'employment': 'full_time', 'employer': 'TechCo', 'income': 78000, 'expenses': 2800, 'kyc': 'verified', 'score': 756, 'grade': 'A+'},
    {'email': 'lisa@co.com', 'phone': '+1-555-321-0987', 'first_name': 'Lisa', 'last_name': 'Park', 'dob': '1988-03-25', 'employment': 'full_time', 'employer': 'FinGroup', 'income': 62000, 'expenses': 2200, 'kyc': 'pending', 'score': None, 'grade': ''},
    {'email': 'tom@inc.com', 'phone': '+1-555-654-3210', 'first_name': 'Tom', 'last_name': 'Wilson', 'dob': '1979-09-12', 'employment': 'full_time', 'employer': 'BigRetail', 'income': 55000, 'expenses': 2100, 'kyc': 'verified', 'score': 612, 'grade': 'C'},
]

for bd in borrowers_data:
    b, created = Borrower.objects.get_or_create(
        institution=inst, email=bd['email'],
        defaults={'phone': bd['phone'], 'kyc_status': bd['kyc'], 'risk_score': bd['score'], 'risk_grade': bd['grade']}
    )
    if created:
        BorrowerProfile.objects.create(
            borrower=b, first_name=bd['first_name'], last_name=bd['last_name'],
            date_of_birth=bd['dob'], employment_status=bd['employment'],
            employer_name=bd['employer'], annual_income=bd['income'], monthly_expenses=bd['expenses'],
        )
        print(f'  Borrower: {bd["first_name"]} {bd["last_name"]}')

# GL Accounts
gl_accounts = [
    ('1000', 'Cash & Equivalents', 'asset'),
    ('1200', 'Loans Receivable', 'asset'),
    ('1300', 'Interest Receivable', 'asset'),
    ('2000', 'Deposits Payable', 'liability'),
    ('2100', 'Accrued Expenses', 'liability'),
    ('3000', 'Retained Earnings', 'equity'),
    ('4100', 'Fee Income', 'revenue'),
    ('4200', 'Interest Income', 'revenue'),
    ('5100', 'Loan Loss Provision', 'expense'),
    ('5200', 'Operating Expenses', 'expense'),
]
for code, name, atype in gl_accounts:
    GLAccount.objects.get_or_create(code=code, defaults={'name': name, 'account_type': atype})

print('\nGL Accounts seeded.')

# Sample loan applications
john = Borrower.objects.get(email='john@example.com', institution=inst)
sarah = Borrower.objects.get(email='sarah@corp.com', institution=inst)

app1, created = LoanApplication.objects.get_or_create(
    institution=inst, borrower=john, product=products['personal'],
    defaults={
        'amount_requested': 25000, 'term_months': 36, 'interest_rate': 8.5,
        'status': 'disbursed', 'risk_grade': 'A', 'risk_score': 742, 'approval_level': 'auto',
        'purpose': 'Debt consolidation', 'amount_approved': 25000,
    }
)
if created:
    from django.utils import timezone
    app1.submitted_at = timezone.now()
    app1.approved_at = timezone.now()
    app1.disbursed_at = timezone.now()
    app1.save()
    from apps.loans.services import disburse_loan
    loan = disburse_loan(app1)
    print(f'  Loan disbursed: {loan}')

app2, created = LoanApplication.objects.get_or_create(
    institution=inst, borrower=sarah, product=products['business'],
    defaults={
        'amount_requested': 75000, 'term_months': 60, 'interest_rate': 6.8,
        'status': 'under_review', 'risk_grade': 'B', 'risk_score': 685, 'approval_level': 'senior_underwriter',
        'purpose': 'Working capital expansion',
    }
)
if created:
    from django.utils import timezone
    app2.submitted_at = timezone.now()
    app2.save()
    print(f'  Application: {app2} (under review)')

print('\nSeed data complete!')
print(f'  Login: http://localhost:8000/admin/')
print(f'  Username: admin')
print(f'  Password: admin123456')
print(f'  API: http://localhost:8000/api/v1/')
