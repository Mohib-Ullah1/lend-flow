from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.core.permissions import IsTenantUser
from .models import KYCVerification
from rest_framework import serializers as drf_serializers

class KYCVerificationSerializer(drf_serializers.ModelSerializer):
    class Meta:
        model = KYCVerification
        fields = '__all__'

class KYCVerificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = KYCVerificationSerializer
    permission_classes = [IsTenantUser]

    def get_queryset(self):
        return KYCVerification.objects.filter(borrower__institution=self.request.user.institution)

class RunKYCView(APIView):
    permission_classes = [IsTenantUser]

    def post(self, request):
        borrower_id = request.data.get('borrower_id')
        if not borrower_id:
            return Response({'error': 'borrower_id required.'}, status=status.HTTP_400_BAD_REQUEST)

        from apps.borrowers.models import Borrower
        try:
            borrower = Borrower.objects.get(id=borrower_id, institution=request.user.institution)
        except Borrower.DoesNotExist:
            return Response({'error': 'Borrower not found.'}, status=status.HTTP_404_NOT_FOUND)

        from .services import run_kyc_pipeline
        results = run_kyc_pipeline(borrower)

        return Response({
            'borrower_id': str(borrower.id),
            'kyc_status': borrower.kyc_status,
            'checks': KYCVerificationSerializer(results, many=True).data,
        }, status=status.HTTP_201_CREATED)
