# Backend Implementation Guide — White-Label Digital Lending Platform

> **Stack**: Django 5.x, DRF, Celery, PostgreSQL 16, Redis, Kafka, Docker/K8s
> **Target**: 8,000+ applications/month, sub-200ms API P95, 99.95% uptime

---

## Table of Contents

1. [Project Structure](#1-project-structure)
2. [Django App Architecture](#2-django-app-architecture)
3. [Database Schema (Advanced)](#3-database-schema-advanced)
4. [Authentication & Authorization](#4-authentication--authorization)
5. [API Design (DRF)](#5-api-design-drf)
6. [Borrower Onboarding & KYC](#6-borrower-onboarding--kyc)
7. [Credit Scoring Engine](#7-credit-scoring-engine)
8. [Loan Origination & Workflow](#8-loan-origination--workflow)
9. [Repayment & Dunning Engine](#9-repayment--dunning-engine)
10. [Double-Entry Ledger](#10-double-entry-ledger)
11. [Investor Module](#11-investor-module)
12. [Event-Driven Architecture](#12-event-driven-architecture)
13. [Multi-Tenancy](#13-multi-tenancy)
14. [Caching Strategy](#14-caching-strategy)
15. [Background Tasks (Celery)](#15-background-tasks-celery)
16. [Real-Time (WebSockets)](#16-real-time-websockets)
17. [Testing Strategy](#17-testing-strategy)
18. [Security Hardening](#18-security-hardening)
19. [Observability & Monitoring](#19-observability--monitoring)
20. [Deployment & Infrastructure](#20-deployment--infrastructure)
21. [Implementation Phases](#21-implementation-phases)

---

## 1. Project Structure

```
lending_platform/
├── config/                        # Project-level settings
│   ├── settings/
│   │   ├── base.py                # Shared settings
│   │   ├── development.py
│   │   ├── staging.py
│   │   └── production.py
│   ├── urls.py                    # Root URL config
│   ├── celery.py                  # Celery app
│   ├── asgi.py                    # ASGI (WebSocket support)
│   └── wsgi.py
├── apps/
│   ├── core/                      # Shared: base models, utils, permissions
│   ├── institutions/              # Multi-tenant institution management
│   ├── accounts/                  # User auth, roles, MFA
│   ├── borrowers/                 # Borrower profiles, onboarding
│   ├── kyc/                       # KYC/AML verification pipeline
│   ├── scoring/                   # Credit scoring & risk engine
│   ├── loans/                     # Loan applications & origination
│   ├── repayments/                # Schedules, payments, dunning
│   ├── ledger/                    # Double-entry accounting
│   ├── investors/                 # Investor portfolios & analytics
│   ├── documents/                 # Document management & OCR
│   ├── notifications/             # SMS, email, push, in-app
│   ├── webhooks/                  # Inbound/outbound webhook handling
│   ├── reports/                   # Scheduled & on-demand reports
│   └── audit/                     # Immutable audit trail
├── services/                      # Business logic layer (service classes)
├── integrations/                  # External API adapters
│   ├── credit_bureaus/
│   ├── payment_gateways/
│   ├── identity_verification/
│   ├── sanctions/
│   └── communication/
├── infrastructure/
│   ├── docker/
│   │   ├── Dockerfile
│   │   ├── Dockerfile.celery
│   │   └── docker-compose.yml
│   ├── k8s/
│   │   ├── deployments/
│   │   ├── services/
│   │   ├── ingress/
│   │   └── configmaps/
│   └── terraform/
├── scripts/                       # Management & migration scripts
├── tests/                         # Top-level test config
├── manage.py
├── requirements/
│   ├── base.txt
│   ├── development.txt
│   ├── production.txt
│   └── testing.txt
└── pyproject.toml
```

---

## 2. Django App Architecture

### Design Principles

- **Fat Services, Thin Views**: Views/serializers handle HTTP; business logic lives in `services/`.
- **Repository Pattern**: Database queries abstracted behind repository classes for testability.
- **Domain Events**: Key state changes emit events consumed by other modules.
- **CQRS**: Separate serializers for read (list/detail) and write (create/update) operations.

### Base Model (all models inherit)

```python
# apps/core/models.py
import uuid
from django.db import models

class TimeStampedModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']

class TenantModel(TimeStampedModel):
    """All tenant-scoped models inherit this."""
    institution = models.ForeignKey(
        'institutions.Institution',
        on_delete=models.CASCADE,
        related_name='%(class)ss',
        db_index=True,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.institution_id:
            raise ValueError("institution is required")
        super().save(*args, **kwargs)
```

### Service Layer Pattern

```python
# services/loan_service.py
from dataclasses import dataclass
from decimal import Decimal
from apps.loans.repositories import LoanApplicationRepository
from apps.scoring.services import ScoringService
from apps.core.events import emit_event

@dataclass
class LoanApplicationResult:
    application_id: str
    status: str
    risk_grade: str
    approved_amount: Decimal | None

class LoanApplicationService:
    def __init__(self):
        self.repo = LoanApplicationRepository()
        self.scoring = ScoringService()

    def submit_application(self, borrower_id: str, data: dict) -> LoanApplicationResult:
        application = self.repo.create(borrower_id=borrower_id, **data)
        score_result = self.scoring.evaluate(application)
        application = self.repo.update_risk(application.id, score_result)

        if score_result.auto_approve:
            application = self.repo.approve(application.id, level='auto')
            emit_event('loan.approved', {'application_id': str(application.id)})

        return LoanApplicationResult(
            application_id=str(application.id),
            status=application.status,
            risk_grade=application.risk_grade,
            approved_amount=application.approved_amount,
        )
```

---

## 3. Database Schema (Advanced)

### Enums (defined as Django TextChoices)

```python
# apps/core/choices.py
from django.db import models

class KYCStatus(models.TextChoices):
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    VERIFIED = 'verified'
    REJECTED = 'rejected'
    EXPIRED = 'expired'

class LoanStatus(models.TextChoices):
    DRAFT = 'draft'
    SUBMITTED = 'submitted'
    UNDER_REVIEW = 'under_review'
    CONDITIONALLY_APPROVED = 'conditionally_approved'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    DISBURSED = 'disbursed'
    CANCELLED = 'cancelled'

class ActiveLoanStatus(models.TextChoices):
    ACTIVE = 'active'
    PAID_OFF = 'paid_off'
    DELINQUENT = 'delinquent'
    DEFAULTED = 'defaulted'
    RESTRUCTURED = 'restructured'
    WRITTEN_OFF = 'written_off'

class RiskGrade(models.TextChoices):
    A_PLUS = 'A+'
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    E = 'E'

class ProductType(models.TextChoices):
    PERSONAL = 'personal'
    BUSINESS = 'business'
    AUTO = 'auto'
    MORTGAGE = 'mortgage'
    LINE_OF_CREDIT = 'line_of_credit'
    INVOICE_FINANCING = 'invoice_financing'
    BNPL = 'buy_now_pay_later'

class RepaymentType(models.TextChoices):
    EMI = 'emi'                  # Equal Monthly Installment
    BULLET = 'bullet'            # Lump sum at end
    BALLOON = 'balloon'          # Small payments + large final
    INTEREST_ONLY = 'interest_only'
    CUSTOM = 'custom'

class InstallmentStatus(models.TextChoices):
    SCHEDULED = 'scheduled'
    PENDING = 'pending'
    PAID = 'paid'
    PARTIALLY_PAID = 'partially_paid'
    OVERDUE = 'overdue'
    WAIVED = 'waived'
```

### Institution Model

```python
# apps/institutions/models.py
from django.db import models
from django.core.validators import MinValueValidator
from apps.core.models import TimeStampedModel

class Institution(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    # Branding
    branding = models.JSONField(default=dict, help_text="Colors, logos, themes, fonts")
    custom_domain = models.CharField(max_length=255, blank=True, default='')

    # Product Configuration
    product_config = models.JSONField(default=dict, help_text="Loan types, limits, rates, fees")
    workflow_config = models.JSONField(default=dict, help_text="Approval chains, authority limits")
    scoring_config = models.JSONField(default=dict, help_text="Risk model weights, thresholds")
    dunning_config = models.JSONField(default=dict, help_text="Collection rules, escalation timelines")

    # Compliance
    regulatory_region = models.CharField(max_length=50, default='US')
    compliance_config = models.JSONField(default=dict)

    # API Access
    api_key_hash = models.CharField(max_length=255)
    webhook_url = models.URLField(blank=True, default='')
    webhook_secret_hash = models.CharField(max_length=255, blank=True, default='')

    # Limits
    max_monthly_applications = models.PositiveIntegerField(default=10000)
    max_loan_amount = models.DecimalField(max_digits=14, decimal_places=2, default=500000.00)

    class Meta:
        db_table = 'institutions'
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return self.name
```

### Borrower Models

```python
# apps/borrowers/models.py
from django.db import models
from django.contrib.postgres.fields import ArrayField
from apps.core.models import TenantModel
from apps.core.choices import KYCStatus
from apps.core.encryption import EncryptedCharField

class Borrower(TenantModel):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    kyc_status = models.CharField(max_length=20, choices=KYCStatus.choices, default=KYCStatus.PENDING)
    risk_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    risk_grade = models.CharField(max_length=5, blank=True, default='')
    is_blacklisted = models.BooleanField(default=False)
    blacklist_reason = models.TextField(blank=True, default='')
    tags = ArrayField(models.CharField(max_length=50), default=list, blank=True)

    class Meta:
        db_table = 'borrowers'
        constraints = [
            models.UniqueConstraint(fields=['institution', 'email'], name='unique_borrower_email_per_institution'),
        ]
        indexes = [
            models.Index(fields=['institution', 'kyc_status']),
            models.Index(fields=['email']),
        ]

class BorrowerProfile(models.Model):
    borrower = models.OneToOneField(Borrower, on_delete=models.CASCADE, primary_key=True, related_name='profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    ssn_encrypted = EncryptedCharField(max_length=512)  # Custom encrypted field
    ssn_last4 = models.CharField(max_length=4)
    address = models.JSONField(help_text='{"street","city","state","zip","country"}')
    employment_status = models.CharField(max_length=30)
    employer_name = models.CharField(max_length=255, blank=True, default='')
    job_title = models.CharField(max_length=255, blank=True, default='')
    annual_income = models.DecimalField(max_digits=14, decimal_places=2)
    monthly_expenses = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    credit_bureau_data = models.JSONField(null=True, blank=True)
    income_verified = models.BooleanField(default=False)
    income_verified_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'borrower_profiles'

class BorrowerDocument(TenantModel):
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=50)  # id_front, id_back, proof_of_address, pay_stub, etc.
    file = models.FileField(upload_to='borrower_docs/%Y/%m/')
    file_hash = models.CharField(max_length=64)  # SHA-256 for integrity
    ocr_data = models.JSONField(null=True, blank=True)
    verification_status = models.CharField(max_length=20, default='pending')
    verified_by = models.CharField(max_length=100, blank=True, default='')  # system or user ID
    expires_at = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'borrower_documents'
```

### Loan Models

```python
# apps/loans/models.py
from django.db import models
from django_fsm import FSMField, transition
from apps.core.models import TenantModel
from apps.core.choices import LoanStatus, ActiveLoanStatus, RiskGrade, ProductType, RepaymentType

class LoanProduct(TenantModel):
    """Configurable loan product per institution."""
    name = models.CharField(max_length=100)
    product_type = models.CharField(max_length=30, choices=ProductType.choices)
    min_amount = models.DecimalField(max_digits=14, decimal_places=2)
    max_amount = models.DecimalField(max_digits=14, decimal_places=2)
    min_term_months = models.PositiveIntegerField()
    max_term_months = models.PositiveIntegerField()
    base_interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    rate_spread_by_grade = models.JSONField(default=dict, help_text='{"A+": 0, "A": 0.5, "B": 1.5, ...}')
    origination_fee_pct = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    late_fee_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    late_fee_grace_days = models.PositiveIntegerField(default=5)
    repayment_type = models.CharField(max_length=20, choices=RepaymentType.choices, default=RepaymentType.EMI)
    requires_collateral = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'loan_products'
        constraints = [
            models.CheckConstraint(check=models.Q(min_amount__lte=models.F('max_amount')), name='min_lte_max_amount'),
            models.CheckConstraint(check=models.Q(min_term_months__lte=models.F('max_term_months')), name='min_lte_max_term'),
        ]

class LoanApplication(TenantModel):
    borrower = models.ForeignKey('borrowers.Borrower', on_delete=models.PROTECT, related_name='applications')
    product = models.ForeignKey(LoanProduct, on_delete=models.PROTECT)
    amount_requested = models.DecimalField(max_digits=14, decimal_places=2)
    amount_approved = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    term_months = models.PositiveIntegerField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    purpose = models.TextField(blank=True, default='')

    # State machine
    status = FSMField(default=LoanStatus.DRAFT, choices=LoanStatus.choices)

    # Risk assessment
    risk_grade = models.CharField(max_length=5, choices=RiskGrade.choices, blank=True, default='')
    risk_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    risk_factors = models.JSONField(default=list)
    approval_level = models.CharField(max_length=20, blank=True, default='')
    decision_reason = models.TextField(blank=True, default='')

    # Timestamps
    submitted_at = models.DateTimeField(null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    rejected_at = models.DateTimeField(null=True, blank=True)
    disbursed_at = models.DateTimeField(null=True, blank=True)

    # Reviewer
    reviewed_by = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_applications'
    )

    class Meta:
        db_table = 'loan_applications'
        indexes = [
            models.Index(fields=['institution', 'status']),
            models.Index(fields=['borrower', 'status']),
            models.Index(fields=['submitted_at']),
        ]

    # --- FSM Transitions ---

    @transition(field=status, source=LoanStatus.DRAFT, target=LoanStatus.SUBMITTED)
    def submit(self):
        from django.utils import timezone
        self.submitted_at = timezone.now()

    @transition(field=status, source=LoanStatus.SUBMITTED, target=LoanStatus.UNDER_REVIEW)
    def start_review(self):
        pass

    @transition(field=status, source=[LoanStatus.UNDER_REVIEW, LoanStatus.SUBMITTED], target=LoanStatus.APPROVED)
    def approve(self, reviewer=None, amount=None):
        from django.utils import timezone
        self.approved_at = timezone.now()
        self.reviewed_by = reviewer
        if amount:
            self.amount_approved = amount

    @transition(field=status, source=[LoanStatus.UNDER_REVIEW, LoanStatus.SUBMITTED], target=LoanStatus.REJECTED)
    def reject(self, reviewer=None, reason=''):
        from django.utils import timezone
        self.rejected_at = timezone.now()
        self.reviewed_by = reviewer
        self.decision_reason = reason

    @transition(field=status, source=LoanStatus.APPROVED, target=LoanStatus.DISBURSED)
    def disburse(self):
        from django.utils import timezone
        self.disbursed_at = timezone.now()

class Loan(TenantModel):
    application = models.OneToOneField(LoanApplication, on_delete=models.PROTECT, related_name='loan')
    borrower = models.ForeignKey('borrowers.Borrower', on_delete=models.PROTECT, related_name='loans')
    product = models.ForeignKey(LoanProduct, on_delete=models.PROTECT)

    # Financial
    principal_amount = models.DecimalField(max_digits=14, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    term_months = models.PositiveIntegerField()
    origination_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_interest = models.DecimalField(max_digits=14, decimal_places=2)
    total_payable = models.DecimalField(max_digits=14, decimal_places=2)
    outstanding_principal = models.DecimalField(max_digits=14, decimal_places=2)
    outstanding_interest = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    outstanding_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Dates
    disbursement_date = models.DateField()
    first_payment_date = models.DateField()
    maturity_date = models.DateField()

    # Status
    status = models.CharField(max_length=20, choices=ActiveLoanStatus.choices, default=ActiveLoanStatus.ACTIVE)
    days_past_due = models.PositiveIntegerField(default=0)
    last_payment_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'loans'
        indexes = [
            models.Index(fields=['institution', 'status']),
            models.Index(fields=['borrower', 'status']),
            models.Index(fields=['maturity_date']),
            models.Index(fields=['days_past_due']),
        ]
```

### Repayment Models

```python
# apps/repayments/models.py
from django.db import models
from apps.core.models import TimeStampedModel
from apps.core.choices import InstallmentStatus

class RepaymentSchedule(TimeStampedModel):
    loan = models.ForeignKey('loans.Loan', on_delete=models.CASCADE, related_name='schedule')
    installment_number = models.PositiveIntegerField()
    due_date = models.DateField()
    amount_due = models.DecimalField(max_digits=14, decimal_places=2)
    principal_component = models.DecimalField(max_digits=14, decimal_places=2)
    interest_component = models.DecimalField(max_digits=14, decimal_places=2)
    fee_component = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount_paid = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=InstallmentStatus.choices, default=InstallmentStatus.SCHEDULED)
    paid_at = models.DateTimeField(null=True, blank=True)
    days_overdue = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'repayment_schedules'
        ordering = ['loan', 'installment_number']
        constraints = [
            models.UniqueConstraint(fields=['loan', 'installment_number'], name='unique_installment'),
        ]
        indexes = [
            models.Index(fields=['due_date', 'status']),
        ]

class Payment(TimeStampedModel):
    loan = models.ForeignKey('loans.Loan', on_delete=models.PROTECT, related_name='payments')
    installment = models.ForeignKey(RepaymentSchedule, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    payment_method = models.CharField(max_length=30)  # ach, card, wire, check
    payment_reference = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=20)  # pending, completed, failed, reversed
    gateway_response = models.JSONField(default=dict)
    processed_at = models.DateTimeField(null=True, blank=True)
    failure_reason = models.TextField(blank=True, default='')

    class Meta:
        db_table = 'payments'
```

### Ledger Models

```python
# apps/ledger/models.py
from django.db import models
from apps.core.models import TimeStampedModel

class GLAccount(TimeStampedModel):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    account_type = models.CharField(max_length=20)  # asset, liability, equity, revenue, expense
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'gl_accounts'

class JournalEntry(TimeStampedModel):
    """Each financial event produces one journal entry with 2+ lines that must balance."""
    institution = models.ForeignKey('institutions.Institution', on_delete=models.CASCADE)
    reference_type = models.CharField(max_length=50)  # disbursement, payment, fee, adjustment
    reference_id = models.UUIDField()
    description = models.TextField()
    entry_date = models.DateField()
    is_reversed = models.BooleanField(default=False)
    reversed_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'journal_entries'
        indexes = [
            models.Index(fields=['institution', 'entry_date']),
            models.Index(fields=['reference_type', 'reference_id']),
        ]

class JournalLine(models.Model):
    id = models.BigAutoField(primary_key=True)
    entry = models.ForeignKey(JournalEntry, on_delete=models.CASCADE, related_name='lines')
    account = models.ForeignKey(GLAccount, on_delete=models.PROTECT)
    debit = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    class Meta:
        db_table = 'journal_lines'

    def clean(self):
        if self.debit and self.credit:
            raise ValueError("A line cannot have both debit and credit.")
```

### Audit Trail

```python
# apps/audit/models.py
from django.db import models
import hashlib, json

class AuditLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    institution_id = models.UUIDField(db_index=True)
    user_id = models.UUIDField(null=True, blank=True)
    action = models.CharField(max_length=50)  # create, update, delete, login, approve, reject
    resource_type = models.CharField(max_length=50)
    resource_id = models.CharField(max_length=100)
    changes = models.JSONField(default=dict)  # {field: {old, new}}
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, default='')
    integrity_hash = models.CharField(max_length=64)  # SHA-256 chain

    class Meta:
        db_table = 'audit_logs'
        indexes = [
            models.Index(fields=['institution_id', 'timestamp']),
            models.Index(fields=['resource_type', 'resource_id']),
        ]

    def save(self, *args, **kwargs):
        if not self.integrity_hash:
            payload = json.dumps({
                'timestamp': str(self.timestamp),
                'action': self.action,
                'resource_type': self.resource_type,
                'resource_id': self.resource_id,
                'changes': self.changes,
            }, sort_keys=True)
            self.integrity_hash = hashlib.sha256(payload.encode()).hexdigest()
        super().save(*args, **kwargs)
```

### Database-Level Optimizations

```sql
-- Partitioning: repayment_schedules by year
CREATE TABLE repayment_schedules (
    -- columns as above
) PARTITION BY RANGE (due_date);

CREATE TABLE repayment_schedules_2025 PARTITION OF repayment_schedules
    FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');
CREATE TABLE repayment_schedules_2026 PARTITION OF repayment_schedules
    FOR VALUES FROM ('2026-01-01') TO ('2027-01-01');

-- Partitioning: journal_lines by month
CREATE TABLE journal_lines (
    -- columns as above
) PARTITION BY RANGE (id);

-- Composite indexes for common queries
CREATE INDEX idx_loans_institution_status ON loans (institution_id, status);
CREATE INDEX idx_repayments_due_status ON repayment_schedules (due_date, status) WHERE status IN ('scheduled', 'pending', 'overdue');

-- Partial index for active loans only
CREATE INDEX idx_active_loans ON loans (institution_id, outstanding_principal) WHERE status = 'active';
```

---

## 4. Authentication & Authorization

### User Model

```python
# apps/accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    institution = models.ForeignKey('institutions.Institution', on_delete=models.CASCADE, null=True, blank=True)
    role = models.CharField(max_length=30, choices=[
        ('super_admin', 'Super Admin'),
        ('institution_admin', 'Institution Admin'),
        ('senior_underwriter', 'Senior Underwriter'),
        ('junior_underwriter', 'Junior Underwriter'),
        ('collections_agent', 'Collections Agent'),
        ('analyst', 'Analyst'),
        ('borrower', 'Borrower'),
        ('investor', 'Investor'),
        ('api_service', 'API Service'),
    ])
    mfa_enabled = models.BooleanField(default=False)
    mfa_secret_encrypted = models.CharField(max_length=512, blank=True, default='')
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    failed_login_attempts = models.PositiveIntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'users'
```

### Permission System

```python
# apps/core/permissions.py
from rest_framework.permissions import BasePermission

class IsTenantUser(BasePermission):
    """Ensures user can only access their institution's data."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.institution_id is not None

class RolePermission(BasePermission):
    """Role-based access: set `required_roles` on the view."""
    def has_permission(self, request, view):
        required = getattr(view, 'required_roles', [])
        return request.user.role in required

# Middleware for automatic tenant scoping
class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated:
            request.tenant = request.user.institution
        return self.get_response(request)
```

### JWT Setup (SimpleJWT)

```python
# config/settings/base.py (excerpt)
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'SIGNING_KEY': env('JWT_SIGNING_KEY'),
    'AUTH_HEADER_TYPES': ('Bearer',),
    'TOKEN_OBTAIN_SERIALIZER': 'apps.accounts.serializers.CustomTokenObtainSerializer',
}
```

---

## 5. API Design (DRF)

### URL Structure

```
/api/v1/
├── auth/
│   ├── token/                     POST   - obtain JWT
│   ├── token/refresh/             POST   - refresh JWT
│   ├── mfa/setup/                 POST   - enable MFA
│   └── mfa/verify/                POST   - verify MFA code
├── institutions/
│   ├── /                          GET    - list (super_admin only)
│   ├── {id}/                      GET    - detail
│   ├── {id}/config/               PATCH  - update config
│   └── {id}/stats/                GET    - dashboard stats
├── borrowers/
│   ├── /                          GET/POST
│   ├── {id}/                      GET/PATCH
│   ├── {id}/kyc/                  POST   - initiate KYC
│   ├── {id}/documents/            GET/POST
│   └── {id}/applications/         GET
├── applications/
│   ├── /                          GET/POST
│   ├── {id}/                      GET/PATCH
│   ├── {id}/submit/               POST   - submit for review
│   ├── {id}/approve/              POST   - approve
│   ├── {id}/reject/               POST   - reject
│   └── {id}/disburse/             POST   - trigger disbursement
├── loans/
│   ├── /                          GET
│   ├── {id}/                      GET
│   ├── {id}/schedule/             GET    - repayment schedule
│   ├── {id}/payments/             GET/POST
│   └── {id}/restructure/          POST
├── ledger/
│   ├── entries/                   GET
│   ├── accounts/                  GET
│   └── reconciliation/            POST
├── investors/
│   ├── portfolio/                 GET
│   ├── portfolio/performance/     GET
│   └── reports/                   GET/POST
├── reports/
│   ├── generate/                  POST
│   └── {id}/download/             GET
└── webhooks/
    ├── /                          GET/POST
    └── {id}/                      GET/DELETE
```

### Serializer Pattern (CQRS)

```python
# apps/loans/serializers.py
from rest_framework import serializers
from apps.loans.models import LoanApplication

class LoanApplicationListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views."""
    borrower_name = serializers.CharField(source='borrower.profile.full_name', read_only=True)

    class Meta:
        model = LoanApplication
        fields = ['id', 'borrower_name', 'amount_requested', 'status', 'risk_grade', 'submitted_at']

class LoanApplicationDetailSerializer(serializers.ModelSerializer):
    """Full serializer for detail views."""
    borrower = BorrowerSummarySerializer(read_only=True)
    product = LoanProductSerializer(read_only=True)
    risk_factors = serializers.JSONField(read_only=True)

    class Meta:
        model = LoanApplication
        fields = '__all__'
        read_only_fields = ['status', 'risk_grade', 'risk_score', 'approved_at', 'rejected_at']

class LoanApplicationCreateSerializer(serializers.ModelSerializer):
    """Write serializer with validation."""
    class Meta:
        model = LoanApplication
        fields = ['borrower', 'product', 'amount_requested', 'term_months', 'purpose']

    def validate(self, data):
        product = data['product']
        if not product.min_amount <= data['amount_requested'] <= product.max_amount:
            raise serializers.ValidationError(
                f"Amount must be between {product.min_amount} and {product.max_amount}"
            )
        if not product.min_term_months <= data['term_months'] <= product.max_term_months:
            raise serializers.ValidationError(
                f"Term must be between {product.min_term_months} and {product.max_term_months} months"
            )
        return data
```

### Pagination & Filtering

```python
# apps/core/pagination.py
from rest_framework.pagination import CursorPagination

class StandardCursorPagination(CursorPagination):
    page_size = 25
    max_page_size = 100
    ordering = '-created_at'

# apps/loans/filters.py
import django_filters
from apps.loans.models import LoanApplication

class LoanApplicationFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=LoanStatus.choices)
    risk_grade = django_filters.ChoiceFilter(choices=RiskGrade.choices)
    amount_min = django_filters.NumberFilter(field_name='amount_requested', lookup_expr='gte')
    amount_max = django_filters.NumberFilter(field_name='amount_requested', lookup_expr='lte')
    submitted_after = django_filters.DateTimeFilter(field_name='submitted_at', lookup_expr='gte')
    submitted_before = django_filters.DateTimeFilter(field_name='submitted_at', lookup_expr='lte')

    class Meta:
        model = LoanApplication
        fields = ['status', 'risk_grade', 'product__product_type']
```

### Throttling

```python
# config/settings/base.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.ScopedRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'auth': '5/minute',
        'borrower_create': '10/hour',
        'application_submit': '20/hour',
        'general': '100/minute',
    },
}
```

---

## 6. Borrower Onboarding & KYC

### KYC Pipeline (Celery Chain)

```python
# apps/kyc/tasks.py
from celery import chain, group
from config.celery import app

@app.task(bind=True, max_retries=3)
def verify_identity_document(self, borrower_id, document_id):
    """OCR + facial recognition via Jumio/ID.me."""
    from integrations.identity_verification import IdentityVerifier
    verifier = IdentityVerifier()
    result = verifier.verify_document(document_id)
    return {'borrower_id': borrower_id, 'document_verified': result.passed, 'ocr_data': result.data}

@app.task(bind=True, max_retries=3)
def screen_sanctions(self, borrower_id):
    """OFAC, EU, UN sanctions screening."""
    from integrations.sanctions import SanctionsScreener
    screener = SanctionsScreener()
    return screener.screen(borrower_id)

@app.task(bind=True, max_retries=3)
def verify_income(self, borrower_id):
    """Verify income via payroll APIs or bank statement analysis."""
    from integrations.income_verification import IncomeVerifier
    verifier = IncomeVerifier()
    return verifier.verify(borrower_id)

@app.task
def compile_kyc_result(results, borrower_id):
    """Aggregate all verification results and make KYC decision."""
    from apps.kyc.services import KYCDecisionService
    service = KYCDecisionService()
    service.decide(borrower_id, results)

def run_kyc_pipeline(borrower_id, document_id):
    """Orchestrate full KYC: parallel checks -> compile decision."""
    pipeline = chain(
        group(
            verify_identity_document.s(borrower_id, document_id),
            screen_sanctions.s(borrower_id),
            verify_income.s(borrower_id),
        ),
        compile_kyc_result.s(borrower_id=borrower_id),
    )
    pipeline.apply_async()
```

---

## 7. Credit Scoring Engine

```python
# apps/scoring/engine.py
from dataclasses import dataclass
from decimal import Decimal

@dataclass
class ScoreResult:
    score: Decimal
    grade: str
    confidence: float
    factors: list[dict]
    auto_approve: bool
    suggested_amount: Decimal | None
    suggested_rate: Decimal

class ScoringEngine:
    GRADE_THRESHOLDS = [
        (850, 'A+'), (750, 'A'), (680, 'B'), (620, 'C'), (550, 'D'), (0, 'E'),
    ]

    def __init__(self, institution_config: dict):
        self.config = institution_config
        self.weights = institution_config.get('score_weights', {
            'bureau_score': 0.35,
            'dti_ratio': 0.20,
            'employment_stability': 0.15,
            'payment_history': 0.15,
            'income_level': 0.10,
            'behavioral': 0.05,
        })

    def evaluate(self, application, bureau_data: dict, profile) -> ScoreResult:
        factors = []
        weighted_score = Decimal('0')

        # Bureau score (normalized to 0-100)
        bureau_normalized = self._normalize_bureau(bureau_data.get('score', 0))
        weighted_score += bureau_normalized * Decimal(str(self.weights['bureau_score']))
        factors.append({'factor': 'bureau_score', 'value': bureau_data.get('score'), 'impact': 'positive' if bureau_normalized > 70 else 'negative'})

        # DTI ratio
        dti = self._calculate_dti(profile.annual_income, profile.monthly_expenses, application.amount_requested, application.term_months)
        dti_score = self._score_dti(dti)
        weighted_score += dti_score * Decimal(str(self.weights['dti_ratio']))
        factors.append({'factor': 'dti_ratio', 'value': float(dti), 'impact': 'positive' if dti < 0.36 else 'negative'})

        # ... additional scoring factors ...

        internal_score = min(weighted_score * 10, Decimal('850'))
        grade = self._assign_grade(internal_score)

        auto_threshold = self.config.get('auto_approve_threshold', 750)
        auto_max_amount = self.config.get('auto_approve_max_amount', 10000)

        return ScoreResult(
            score=internal_score,
            grade=grade,
            confidence=0.92,
            factors=factors,
            auto_approve=(internal_score >= auto_threshold and application.amount_requested <= auto_max_amount),
            suggested_amount=application.amount_requested if internal_score >= 550 else None,
            suggested_rate=self._calculate_rate(grade, application.product),
        )

    def _assign_grade(self, score: Decimal) -> str:
        for threshold, grade in self.GRADE_THRESHOLDS:
            if score >= threshold:
                return grade
        return 'E'

    def _calculate_dti(self, annual_income, monthly_expenses, loan_amount, term_months) -> Decimal:
        monthly_income = annual_income / 12
        estimated_payment = loan_amount / term_months
        return (monthly_expenses + estimated_payment) / monthly_income

    def _score_dti(self, dti: Decimal) -> Decimal:
        if dti <= Decimal('0.28'):
            return Decimal('95')
        elif dti <= Decimal('0.36'):
            return Decimal('80')
        elif dti <= Decimal('0.43'):
            return Decimal('60')
        return Decimal('30')

    def _normalize_bureau(self, score: int) -> Decimal:
        return Decimal(str(min(max((score - 300) / 5.5, 0), 100)))

    def _calculate_rate(self, grade: str, product) -> Decimal:
        spread = Decimal(str(product.rate_spread_by_grade.get(grade, 5)))
        return product.base_interest_rate + spread
```

---

## 8. Loan Origination & Workflow

### Approval Pipeline

```python
# apps/loans/workflow.py
from apps.core.events import emit_event

class ApprovalPipeline:
    """Determines approval level based on risk grade, amount, and institution config."""

    def __init__(self, institution):
        self.config = institution.workflow_config

    def route(self, application) -> str:
        rules = self.config.get('approval_rules', [])

        for rule in rules:
            if self._matches(application, rule):
                return rule['approval_level']

        return 'committee'  # default to highest level

    def _matches(self, application, rule) -> bool:
        if 'max_amount' in rule and application.amount_requested > rule['max_amount']:
            return False
        if 'grades' in rule and application.risk_grade not in rule['grades']:
            return False
        return True

    def process(self, application):
        level = self.route(application)
        application.approval_level = level

        if level == 'auto':
            application.approve()
            application.save()
            emit_event('loan.auto_approved', {'application_id': str(application.id)})
        else:
            application.start_review()
            application.save()
            emit_event('loan.queued_for_review', {
                'application_id': str(application.id),
                'level': level,
            })
```

### Example Workflow Config (per institution)

```json
{
  "approval_rules": [
    {"grades": ["A+", "A"], "max_amount": 10000, "approval_level": "auto"},
    {"grades": ["A+", "A"], "max_amount": 50000, "approval_level": "junior_underwriter"},
    {"grades": ["B", "C"], "max_amount": 25000, "approval_level": "junior_underwriter"},
    {"grades": ["B", "C"], "max_amount": 100000, "approval_level": "senior_underwriter"},
    {"grades": ["D", "E"], "approval_level": "senior_underwriter"},
    {"max_amount": 999999999, "approval_level": "committee"}
  ],
  "authority_limits": {
    "junior_underwriter": 50000,
    "senior_underwriter": 250000,
    "committee": 999999999
  }
}
```

---

## 9. Repayment & Dunning Engine

### Schedule Generator

```python
# apps/repayments/calculator.py
from decimal import Decimal, ROUND_HALF_UP
from datetime import date
from dateutil.relativedelta import relativedelta

class EMICalculator:
    @staticmethod
    def generate_schedule(principal: Decimal, annual_rate: Decimal, term_months: int, start_date: date) -> list[dict]:
        monthly_rate = annual_rate / 12 / 100
        if monthly_rate == 0:
            emi = principal / term_months
        else:
            r = monthly_rate
            n = term_months
            emi = principal * (r * (1 + r) ** n) / ((1 + r) ** n - 1)

        emi = emi.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        schedule = []
        remaining = principal

        for i in range(1, term_months + 1):
            interest = (remaining * monthly_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            principal_part = emi - interest
            if i == term_months:
                principal_part = remaining
                emi = principal_part + interest

            remaining -= principal_part
            due_date = start_date + relativedelta(months=i)

            schedule.append({
                'installment_number': i,
                'due_date': due_date,
                'amount_due': emi,
                'principal_component': principal_part,
                'interest_component': interest,
            })

        return schedule
```

### Dunning Automation

```python
# apps/repayments/dunning.py
from celery import shared_task
from datetime import date, timedelta

@shared_task
def run_daily_dunning():
    """Daily job: identify overdue installments and trigger actions."""
    from apps.repayments.models import RepaymentSchedule
    from apps.loans.models import Loan

    today = date.today()

    overdue = RepaymentSchedule.objects.filter(
        due_date__lt=today,
        status__in=['scheduled', 'pending'],
    ).select_related('loan', 'loan__borrower', 'loan__institution')

    for installment in overdue:
        days_overdue = (today - installment.due_date).days
        installment.status = 'overdue'
        installment.days_overdue = days_overdue
        installment.save(update_fields=['status', 'days_overdue'])

        config = installment.loan.institution.dunning_config
        actions = config.get('actions', DEFAULT_DUNNING_ACTIONS)

        for action in actions:
            if days_overdue == action['day']:
                trigger_dunning_action.delay(
                    installment_id=str(installment.id),
                    action_type=action['type'],
                    template=action.get('template', ''),
                )

        # Update loan DPD
        loan = installment.loan
        max_dpd = loan.schedule.filter(status='overdue').aggregate(
            max_dpd=models.Max('days_overdue')
        )['max_dpd'] or 0
        loan.days_past_due = max_dpd

        if max_dpd >= 90:
            loan.status = 'defaulted'
        elif max_dpd > 0:
            loan.status = 'delinquent'
        loan.save(update_fields=['days_past_due', 'status'])

DEFAULT_DUNNING_ACTIONS = [
    {'day': 1, 'type': 'sms', 'template': 'payment_reminder_sms'},
    {'day': 3, 'type': 'email', 'template': 'payment_overdue_email'},
    {'day': 7, 'type': 'sms', 'template': 'payment_urgent_sms'},
    {'day': 14, 'type': 'email', 'template': 'collections_warning_email'},
    {'day': 30, 'type': 'phone_call', 'template': 'collections_call_script'},
    {'day': 60, 'type': 'email', 'template': 'legal_notice_email'},
    {'day': 90, 'type': 'escalation', 'template': 'default_escalation'},
]

@shared_task
def trigger_dunning_action(installment_id, action_type, template):
    from apps.notifications.services import NotificationService
    NotificationService().send_dunning(installment_id, action_type, template)
```

---

## 10. Double-Entry Ledger

```python
# apps/ledger/services.py
from decimal import Decimal
from django.db import transaction
from apps.ledger.models import JournalEntry, JournalLine, GLAccount

class LedgerService:
    # Standard GL account codes
    CASH = '1000'
    LOANS_RECEIVABLE = '1200'
    INTEREST_RECEIVABLE = '1300'
    FEE_INCOME = '4100'
    INTEREST_INCOME = '4200'
    LOAN_LOSS_PROVISION = '5100'

    @transaction.atomic
    def record_disbursement(self, loan):
        entry = JournalEntry.objects.create(
            institution=loan.institution,
            reference_type='disbursement',
            reference_id=loan.id,
            description=f'Loan disbursement: {loan.id}',
            entry_date=loan.disbursement_date,
        )
        JournalLine.objects.bulk_create([
            JournalLine(entry=entry, account=self._get_account(self.LOANS_RECEIVABLE), debit=loan.principal_amount),
            JournalLine(entry=entry, account=self._get_account(self.CASH), credit=loan.principal_amount),
        ])

        if loan.origination_fee > 0:
            fee_entry = JournalEntry.objects.create(
                institution=loan.institution,
                reference_type='origination_fee',
                reference_id=loan.id,
                description=f'Origination fee: {loan.id}',
                entry_date=loan.disbursement_date,
            )
            JournalLine.objects.bulk_create([
                JournalLine(entry=fee_entry, account=self._get_account(self.CASH), debit=loan.origination_fee),
                JournalLine(entry=fee_entry, account=self._get_account(self.FEE_INCOME), credit=loan.origination_fee),
            ])

    @transaction.atomic
    def record_payment(self, payment, principal_part: Decimal, interest_part: Decimal):
        entry = JournalEntry.objects.create(
            institution=payment.loan.institution,
            reference_type='payment',
            reference_id=payment.id,
            description=f'Payment received: {payment.payment_reference}',
            entry_date=payment.processed_at.date(),
        )
        lines = [
            JournalLine(entry=entry, account=self._get_account(self.CASH), debit=payment.amount),
            JournalLine(entry=entry, account=self._get_account(self.LOANS_RECEIVABLE), credit=principal_part),
        ]
        if interest_part > 0:
            lines.append(
                JournalLine(entry=entry, account=self._get_account(self.INTEREST_INCOME), credit=interest_part)
            )
        JournalLine.objects.bulk_create(lines)

    def _get_account(self, code: str) -> GLAccount:
        return GLAccount.objects.get(code=code)
```

---

## 11. Investor Module

```python
# apps/investors/models.py
from django.db import models
from django.contrib.postgres.fields import ArrayField
from apps.core.models import TenantModel

class Investor(TenantModel):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE)
    investor_type = models.CharField(max_length=30)  # individual, institutional, fund
    accredited = models.BooleanField(default=False)
    investment_preferences = models.JSONField(default=dict)

    class Meta:
        db_table = 'investors'

class InvestorPortfolio(TenantModel):
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE, related_name='portfolios')
    name = models.CharField(max_length=100)

    # Metrics (recalculated daily)
    total_invested = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    current_value = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total_returns = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    irr = models.DecimalField(max_digits=7, decimal_places=4, null=True, blank=True)
    xirr = models.DecimalField(max_digits=7, decimal_places=4, null=True, blank=True)

    # Risk metrics
    par_30 = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # % portfolio > 30 days overdue
    par_60 = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    par_90 = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    default_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    expected_loss = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    class Meta:
        db_table = 'investor_portfolios'

class Investment(TenantModel):
    portfolio = models.ForeignKey(InvestorPortfolio, on_delete=models.CASCADE, related_name='investments')
    loan = models.ForeignKey('loans.Loan', on_delete=models.PROTECT)
    amount_invested = models.DecimalField(max_digits=14, decimal_places=2)
    share_percentage = models.DecimalField(max_digits=5, decimal_places=2)  # % of loan owned
    status = models.CharField(max_length=20, default='active')

    class Meta:
        db_table = 'investments'
        constraints = [
            models.UniqueConstraint(fields=['portfolio', 'loan'], name='unique_portfolio_loan'),
        ]
```

### Portfolio Analytics Task

```python
# apps/investors/tasks.py
from celery import shared_task

@shared_task
def recalculate_portfolio_metrics():
    """Nightly job to update all investor portfolio metrics."""
    from apps.investors.models import InvestorPortfolio
    from apps.investors.analytics import PortfolioAnalytics

    for portfolio in InvestorPortfolio.objects.all():
        analytics = PortfolioAnalytics(portfolio)
        portfolio.total_invested = analytics.total_invested()
        portfolio.current_value = analytics.current_value()
        portfolio.total_returns = analytics.total_returns()
        portfolio.irr = analytics.calculate_irr()
        portfolio.par_30 = analytics.par(30)
        portfolio.par_60 = analytics.par(60)
        portfolio.par_90 = analytics.par(90)
        portfolio.default_rate = analytics.default_rate()
        portfolio.expected_loss = analytics.expected_loss()
        portfolio.save()
```

---

## 12. Event-Driven Architecture

```python
# apps/core/events.py
import json
from django.conf import settings

class EventBus:
    """Abstraction over message broker (Kafka/Redis Streams)."""

    def __init__(self):
        if settings.EVENT_BACKEND == 'kafka':
            from kafka import KafkaProducer
            self.producer = KafkaProducer(
                bootstrap_servers=settings.KAFKA_BROKERS,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            )
        else:
            import redis
            self.redis = redis.from_url(settings.REDIS_URL)

    def emit(self, event_type: str, payload: dict):
        message = {
            'event_type': event_type,
            'payload': payload,
            'timestamp': str(timezone.now()),
        }
        if hasattr(self, 'producer'):
            topic = event_type.split('.')[0]  # e.g., 'loan' from 'loan.approved'
            self.producer.send(topic, value=message)
        else:
            self.redis.xadd(f'events:{event_type}', message)

_bus = None

def emit_event(event_type: str, payload: dict):
    global _bus
    if _bus is None:
        _bus = EventBus()
    _bus.emit(event_type, payload)
```

### Key Events

| Event | Trigger | Consumers |
|-------|---------|-----------|
| `borrower.created` | New borrower registered | KYC module, notifications |
| `kyc.completed` | KYC pipeline finishes | Scoring, borrower profile |
| `loan.submitted` | Application submitted | Scoring engine |
| `loan.scored` | Risk assessment done | Approval pipeline |
| `loan.approved` | Loan approved | Disbursement, notifications |
| `loan.disbursed` | Funds sent | Ledger, repayment scheduler, investors |
| `payment.received` | Payment processed | Ledger, loan balance update |
| `payment.failed` | Payment failed | Dunning, notifications |
| `loan.defaulted` | 90+ DPD | Collections, investor alerts, ledger (provision) |

---

## 13. Multi-Tenancy

```python
# apps/core/managers.py
from django.db import models

class TenantManager(models.Manager):
    def for_tenant(self, institution):
        return self.filter(institution=institution)

# Automatic filtering via middleware + custom queryset
class TenantQuerySet(models.QuerySet):
    def for_request(self, request):
        if hasattr(request, 'tenant') and request.tenant:
            return self.filter(institution=request.tenant)
        return self.none()

# In views, always scope queries:
class LoanApplicationViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return LoanApplication.objects.filter(institution=self.request.user.institution)
```

---

## 14. Caching Strategy

```python
# apps/core/cache.py
from django.core.cache import cache
from functools import wraps

def institution_cache(timeout=300):
    """Cache decorator scoped per institution."""
    def decorator(func):
        @wraps(func)
        def wrapper(self, institution_id, *args, **kwargs):
            key = f"{func.__name__}:{institution_id}:{hash(args)}"
            result = cache.get(key)
            if result is None:
                result = func(self, institution_id, *args, **kwargs)
                cache.set(key, result, timeout)
            return result
        return wrapper
    return decorator

# Cache config in settings
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': env('REDIS_URL'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'SERIALIZER': 'django_redis.serializers.json.JSONSerializer',
        },
        'KEY_PREFIX': 'lending',
        'TIMEOUT': 300,
    }
}
```

### What to Cache

| Data | TTL | Invalidation |
|------|-----|-------------|
| Institution config/branding | 10 min | On config update |
| Loan product listings | 5 min | On product change |
| Dashboard stats | 2 min | Time-based |
| Borrower KYC status | 1 min | On KYC update |
| Rate calculations | 15 min | On rate change |

---

## 15. Background Tasks (Celery)

```python
# config/celery.py
from celery import Celery
from celery.schedules import crontab

app = Celery('lending_platform')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'daily-dunning': {
        'task': 'apps.repayments.dunning.run_daily_dunning',
        'schedule': crontab(hour=6, minute=0),
    },
    'nightly-portfolio-recalc': {
        'task': 'apps.investors.tasks.recalculate_portfolio_metrics',
        'schedule': crontab(hour=2, minute=0),
    },
    'daily-reconciliation': {
        'task': 'apps.ledger.tasks.run_reconciliation',
        'schedule': crontab(hour=3, minute=0),
    },
    'hourly-dpd-update': {
        'task': 'apps.repayments.tasks.update_days_past_due',
        'schedule': crontab(minute=0),
    },
}

# Celery config
CELERY_BROKER_URL = env('REDIS_URL')
CELERY_RESULT_BACKEND = env('REDIS_URL')
CELERY_TASK_SERIALIZER = 'json'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 300
CELERY_WORKER_PREFETCH_MULTIPLIER = 1
CELERY_TASK_ROUTES = {
    'apps.kyc.*': {'queue': 'kyc'},
    'apps.scoring.*': {'queue': 'scoring'},
    'apps.repayments.*': {'queue': 'repayments'},
    'apps.notifications.*': {'queue': 'notifications'},
}
```

---

## 16. Real-Time (WebSockets)

```python
# apps/core/consumers.py
import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer

class DashboardConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.institution_id = self.scope['user'].institution_id
        self.group_name = f'dashboard_{self.institution_id}'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def loan_update(self, event):
        await self.send_json(event['data'])

    async def payment_received(self, event):
        await self.send_json(event['data'])

# Trigger from anywhere:
# async_to_sync(channel_layer.group_send)(f'dashboard_{institution_id}', {
#     'type': 'loan_update',
#     'data': {'application_id': '...', 'new_status': 'approved'}
# })
```

---

## 17. Testing Strategy

```
tests/
├── unit/                    # Pure logic tests (no DB)
│   ├── test_scoring.py
│   ├── test_emi_calculator.py
│   └── test_ledger_logic.py
├── integration/             # DB + service tests
│   ├── test_kyc_pipeline.py
│   ├── test_loan_workflow.py
│   └── test_payment_flow.py
├── api/                     # DRF API tests
│   ├── test_auth.py
│   ├── test_applications.py
│   └── test_borrowers.py
├── e2e/                     # Full flow tests
│   └── test_loan_lifecycle.py
├── factories.py             # factory_boy factories
├── conftest.py              # Shared fixtures
└── fixtures/                # JSON test data
```

```python
# tests/factories.py
import factory
from apps.institutions.models import Institution
from apps.borrowers.models import Borrower, BorrowerProfile
from apps.loans.models import LoanApplication, LoanProduct

class InstitutionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Institution
    name = factory.Sequence(lambda n: f'Bank {n}')
    slug = factory.LazyAttribute(lambda o: o.name.lower().replace(' ', '-'))
    branding = {'primary_color': '#1a56db', 'logo_url': '/static/logo.png'}
    product_config = {}
    workflow_config = {}
    scoring_config = {}
    dunning_config = {}
    api_key_hash = factory.Faker('sha256')

class BorrowerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Borrower
    institution = factory.SubFactory(InstitutionFactory)
    email = factory.Faker('email')
    phone = factory.Faker('phone_number')
```

---

## 18. Security Hardening

### Encryption at Rest

```python
# apps/core/encryption.py
from cryptography.fernet import Fernet
from django.conf import settings
from django.db import models

class EncryptedCharField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 512)
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        if value:
            f = Fernet(settings.FIELD_ENCRYPTION_KEY.encode())
            return f.encrypt(value.encode()).decode()
        return value

    def from_db_value(self, value, expression, connection):
        if value:
            f = Fernet(settings.FIELD_ENCRYPTION_KEY.encode())
            return f.decrypt(value.encode()).decode()
        return value
```

### Security Middleware

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'apps.core.middleware.TenantMiddleware',
    'apps.core.middleware.AuditMiddleware',
    'apps.core.middleware.RateLimitMiddleware',
    'csp.middleware.CSPMiddleware',
    # ...
]

# Security headers
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSP_DEFAULT_SRC = ("'self'",)
```

---

## 19. Observability & Monitoring

```python
# Structured logging
LOGGING = {
    'version': 1,
    'handlers': {
        'json': {
            'class': 'pythonjsonlogger.jsonlogger.JsonFormatter',
        },
    },
    'loggers': {
        'apps': {'handlers': ['json'], 'level': 'INFO'},
    },
}

# Prometheus metrics
# apps/core/metrics.py
from prometheus_client import Counter, Histogram

loan_applications_total = Counter(
    'loan_applications_total', 'Total loan applications', ['institution', 'status']
)
scoring_duration = Histogram(
    'scoring_duration_seconds', 'Time to score an application', ['institution']
)
payment_processing_duration = Histogram(
    'payment_processing_seconds', 'Time to process a payment', ['method']
)
```

### Health Check

```python
# apps/core/views.py
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache

def health_check(request):
    checks = {}
    try:
        connection.ensure_connection()
        checks['database'] = 'ok'
    except Exception:
        checks['database'] = 'error'
    try:
        cache.set('health', 'ok', 5)
        checks['cache'] = 'ok' if cache.get('health') == 'ok' else 'error'
    except Exception:
        checks['cache'] = 'error'

    status = 200 if all(v == 'ok' for v in checks.values()) else 503
    return JsonResponse({'status': 'healthy' if status == 200 else 'degraded', 'checks': checks}, status=status)
```

---

## 20. Deployment & Infrastructure

### Docker

```dockerfile
# infrastructure/docker/Dockerfile
FROM python:3.12-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev && rm -rf /var/lib/apt/lists/*
COPY requirements/production.txt .
RUN pip install --no-cache-dir -r production.txt
COPY . .
RUN python manage.py collectstatic --noinput

FROM base AS web
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120"]

FROM base AS celery-worker
CMD ["celery", "-A", "config", "worker", "-l", "info", "--concurrency", "4"]

FROM base AS celery-beat
CMD ["celery", "-A", "config", "beat", "-l", "info"]
```

### docker-compose.yml

```yaml
version: "3.9"
services:
  web:
    build: {context: ../.., dockerfile: infrastructure/docker/Dockerfile, target: web}
    ports: ["8000:8000"]
    env_file: .env
    depends_on: [db, redis]

  celery-worker:
    build: {context: ../.., dockerfile: infrastructure/docker/Dockerfile, target: celery-worker}
    env_file: .env
    depends_on: [db, redis]

  celery-beat:
    build: {context: ../.., dockerfile: infrastructure/docker/Dockerfile, target: celery-beat}
    env_file: .env
    depends_on: [db, redis]

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: lending_platform
      POSTGRES_USER: lending
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes: [postgres_data:/var/lib/postgresql/data]
    ports: ["5432:5432"]

  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]

volumes:
  postgres_data:
```

### Requirements (production.txt)

```
Django==5.1.*
djangorestframework==3.15.*
django-filter==24.*
djangorestframework-simplejwt==5.*
django-cors-headers==4.*
django-fsm==3.*
django-redis==5.*
django-environ==0.11.*
celery[redis]==5.*
channels[daphne]==4.*
channels-redis==4.*
psycopg[binary]==3.*
cryptography==43.*
python-dateutil==2.*
factory-boy==3.*
sentry-sdk[django]==2.*
prometheus-client==0.*
python-json-logger==2.*
gunicorn==22.*
```

---

## 21. Implementation Phases

### Phase 1 — Foundation (Weeks 1-2)
- [ ] Django project scaffold with settings split
- [ ] Docker + docker-compose setup
- [ ] Core app: base models, encryption, permissions, middleware
- [ ] Institution model + admin
- [ ] User model with JWT auth + MFA
- [ ] Audit log infrastructure
- [ ] Health check endpoint
- [ ] CI/CD pipeline (GitHub Actions)

### Phase 2 — Borrower & KYC (Weeks 3-4)
- [ ] Borrower models + CRUD API
- [ ] Document upload + S3 storage
- [ ] KYC pipeline (Celery tasks)
- [ ] Integration adapters: identity verification, sanctions
- [ ] Notification service (email + SMS)
- [ ] Borrower onboarding API flow

### Phase 3 — Scoring & Origination (Weeks 5-6)
- [ ] Loan product configuration
- [ ] Credit scoring engine
- [ ] Bureau integration adapters
- [ ] Loan application CRUD + FSM transitions
- [ ] Approval pipeline with routing rules
- [ ] Underwriter queue API

### Phase 4 — Disbursement & Repayments (Weeks 7-8)
- [ ] Disbursement flow + payment gateway integration
- [ ] EMI/Bullet/Balloon schedule generators
- [ ] Repayment processing + payment recording
- [ ] Dunning engine (daily Celery beat)
- [ ] Late fee calculation
- [ ] Loan status lifecycle management

### Phase 5 — Ledger & Reconciliation (Weeks 9-10)
- [ ] GL accounts setup
- [ ] Journal entry service (disbursement, payment, fees)
- [ ] Daily reconciliation job
- [ ] Ledger API endpoints
- [ ] Financial reporting queries

### Phase 6 — Investors & Analytics (Weeks 11-12)
- [ ] Investor models + portfolio management
- [ ] Investment allocation
- [ ] Portfolio metrics calculation (IRR, PAR, default rate)
- [ ] Analytics API endpoints
- [ ] Report generation (PDF/Excel)

### Phase 7 — White-Label & Scale (Weeks 13-14)
- [ ] Multi-tenant branding engine
- [ ] Custom domain support
- [ ] WebSocket real-time updates
- [ ] Event bus (Kafka/Redis Streams)
- [ ] Performance tuning: query optimization, caching, read replicas
- [ ] Load testing + horizontal scaling validation
- [ ] Prometheus/Grafana dashboards
- [ ] Production hardening + security audit
