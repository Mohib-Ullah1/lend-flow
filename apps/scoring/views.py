from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.core.permissions import IsTenantUser
from .models import CreditScore
from .serializers import CreditScoreSerializer, ScoreRequestSerializer
from .engine import score_application

class CreditScoreViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CreditScoreSerializer
    permission_classes = [IsTenantUser]

    def get_queryset(self):
        return CreditScore.objects.filter(borrower__institution=self.request.user.institution)

class ScoreApplicationView(APIView):
    permission_classes = [IsTenantUser]

    def post(self, request):
        serializer = ScoreRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        from apps.loans.models import LoanApplication
        try:
            app = LoanApplication.objects.select_related('borrower__profile').get(
                id=serializer.validated_data['application_id'],
                institution=request.user.institution,
            )
        except LoanApplication.DoesNotExist:
            return Response({'error': 'Application not found.'}, status=status.HTTP_404_NOT_FOUND)

        result = score_application(app)

        credit_score = CreditScore.objects.create(
            borrower=app.borrower,
            application=app,
            score=result['score'],
            grade=result['grade'],
            confidence=result['confidence'],
            factors=result['factors'],
            bureau_score=result['bureau_score'],
            dti_ratio=result['dti_ratio'],
            auto_approve=result['auto_approve'],
        )

        # Update application
        app.risk_score = result['score']
        app.risk_grade = result['grade']
        app.risk_factors = result['factors']
        app.save(update_fields=['risk_score', 'risk_grade', 'risk_factors'])

        # Update borrower
        app.borrower.risk_score = result['score']
        app.borrower.risk_grade = result['grade']
        app.borrower.save(update_fields=['risk_score', 'risk_grade'])

        return Response(CreditScoreSerializer(credit_score).data, status=status.HTTP_201_CREATED)
