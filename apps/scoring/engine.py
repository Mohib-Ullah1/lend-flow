from decimal import Decimal
import random

GRADE_THRESHOLDS = [(800, 'A+'), (720, 'A'), (680, 'B'), (620, 'C'), (550, 'D'), (0, 'E')]

def assign_grade(score):
    for threshold, grade in GRADE_THRESHOLDS:
        if score >= threshold:
            return grade
    return 'E'

def score_application(application):
    """Score a loan application. Uses rule-based scoring (no external APIs)."""
    borrower = application.borrower
    profile = getattr(borrower, 'profile', None)
    factors = []
    weighted_score = Decimal('0')

    # Factor 1: Existing risk score (if from bureau)
    if borrower.risk_score:
        bureau = float(borrower.risk_score)
        normalized = min(max((bureau - 300) / 5.5, 0), 100)
        weighted_score += Decimal(str(normalized)) * Decimal('0.35')
        factors.append({'factor': 'bureau_score', 'value': bureau, 'weight': 0.35, 'impact': 'positive' if bureau > 700 else 'negative'})
    else:
        # No bureau score, use random simulation
        bureau = random.randint(580, 780)
        normalized = min(max((bureau - 300) / 5.5, 0), 100)
        weighted_score += Decimal(str(normalized)) * Decimal('0.35')
        factors.append({'factor': 'bureau_score', 'value': bureau, 'weight': 0.35, 'impact': 'positive' if bureau > 700 else 'negative'})

    # Factor 2: DTI ratio
    dti = Decimal('0.35')  # default
    if profile and profile.annual_income > 0:
        monthly_income = profile.annual_income / 12
        estimated_payment = application.amount_requested / application.term_months
        monthly_obligations = profile.monthly_expenses + estimated_payment
        dti = monthly_obligations / monthly_income

    if dti <= Decimal('0.28'):
        dti_score = 95
    elif dti <= Decimal('0.36'):
        dti_score = 80
    elif dti <= Decimal('0.43'):
        dti_score = 60
    else:
        dti_score = 30
    weighted_score += Decimal(str(dti_score)) * Decimal('0.25')
    factors.append({'factor': 'dti_ratio', 'value': float(round(dti, 4)), 'weight': 0.25, 'impact': 'positive' if dti < Decimal('0.36') else 'negative'})

    # Factor 3: Employment
    emp_score = 50
    if profile:
        emp_map = {'full_time': 90, 'part_time': 60, 'self_employed': 70, 'contract': 55, 'retired': 65, 'unemployed': 20}
        emp_score = emp_map.get(profile.employment_status, 50)
    weighted_score += Decimal(str(emp_score)) * Decimal('0.20')
    factors.append({'factor': 'employment', 'value': getattr(profile, 'employment_status', 'unknown'), 'weight': 0.20, 'impact': 'positive' if emp_score >= 70 else 'negative'})

    # Factor 4: Income level
    income_score = 50
    if profile and profile.annual_income > 0:
        if profile.annual_income >= 100000: income_score = 95
        elif profile.annual_income >= 75000: income_score = 80
        elif profile.annual_income >= 50000: income_score = 65
        elif profile.annual_income >= 30000: income_score = 45
        else: income_score = 25
    weighted_score += Decimal(str(income_score)) * Decimal('0.20')
    factors.append({'factor': 'income_level', 'value': float(getattr(profile, 'annual_income', 0)), 'weight': 0.20, 'impact': 'positive' if income_score >= 65 else 'negative'})

    # Calculate final score (0-850 scale)
    internal_score = min(float(weighted_score) * 10, 850)
    internal_score = max(internal_score, 300)
    grade = assign_grade(internal_score)

    # Auto-approve logic
    auto_approve = (internal_score >= 720 and float(application.amount_requested) <= 50000)

    return {
        'score': round(internal_score, 2),
        'grade': grade,
        'confidence': 0.85,
        'factors': factors,
        'bureau_score': bureau,
        'dti_ratio': float(round(dti, 4)),
        'auto_approve': auto_approve,
    }
