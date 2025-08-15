from django.utils import timezone

def run_kyc_pipeline(borrower):
    """Simulated KYC pipeline. In production, this calls external APIs."""
    from .models import KYCVerification

    checks = ['identity', 'address', 'sanctions']
    results = []
    all_passed = True

    for check_type in checks:
        kyc = KYCVerification.objects.create(
            borrower=borrower,
            verification_type=check_type,
            status='passed',
            verified_at=timezone.now(),
            result_data={'method': 'simulated', 'confidence': 0.95},
        )
        results.append(kyc)

    if all_passed:
        borrower.kyc_status = 'verified'
    else:
        borrower.kyc_status = 'rejected'
    borrower.save(update_fields=['kyc_status'])

    return results
