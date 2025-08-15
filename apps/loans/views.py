from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from apps.core.permissions import IsTenantUser, RolePermission
from .models import LoanProduct, LoanApplication, Loan
from .serializers import (
    LoanProductSerializer, LoanApplicationListSerializer, LoanApplicationDetailSerializer,
    LoanApplicationCreateSerializer, LoanListSerializer, LoanDetailSerializer,
)

class LoanProductViewSet(viewsets.ModelViewSet):
    serializer_class = LoanProductSerializer
    permission_classes = [IsTenantUser]

    def get_queryset(self):
        return LoanProduct.objects.filter(institution=self.request.user.institution)

    def perform_create(self, serializer):
        serializer.save(institution=self.request.user.institution)


class LoanApplicationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsTenantUser]
    filterset_fields = ['status', 'risk_grade', 'borrower']
    search_fields = ['borrower__email', 'borrower__profile__first_name', 'borrower__profile__last_name']
    ordering_fields = ['created_at', 'amount_requested', 'submitted_at']

    def get_queryset(self):
        qs = LoanApplication.objects.filter(institution=self.request.user.institution).select_related('borrower__profile', 'product')
        if self.request.user.role == 'borrower' and hasattr(self.request.user, 'borrower_profile'):
            qs = qs.filter(borrower=self.request.user.borrower_profile)
        return qs

    def get_serializer_class(self):
        if self.action == 'list':
            return LoanApplicationListSerializer
        if self.action == 'create':
            return LoanApplicationCreateSerializer
        return LoanApplicationDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(LoanApplicationDetailSerializer(instance).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        app = self.get_object()
        if app.status not in ('submitted', 'under_review'):
            return Response({'error': 'Cannot approve this application.'}, status=status.HTTP_400_BAD_REQUEST)
        app.status = 'approved'
        app.approved_at = timezone.now()
        app.reviewed_by = request.user
        app.amount_approved = request.data.get('amount', app.amount_requested)
        app.save()
        return Response(LoanApplicationDetailSerializer(app).data)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        app = self.get_object()
        if app.status not in ('submitted', 'under_review'):
            return Response({'error': 'Cannot reject this application.'}, status=status.HTTP_400_BAD_REQUEST)
        app.status = 'rejected'
        app.rejected_at = timezone.now()
        app.reviewed_by = request.user
        app.decision_reason = request.data.get('reason', '')
        app.save()
        return Response(LoanApplicationDetailSerializer(app).data)

    @action(detail=True, methods=['post'])
    def disburse(self, request, pk=None):
        app = self.get_object()
        if app.status != 'approved':
            return Response({'error': 'Only approved applications can be disbursed.'}, status=status.HTTP_400_BAD_REQUEST)
        from apps.loans.services import disburse_loan
        loan = disburse_loan(app)
        app.status = 'disbursed'
        app.disbursed_at = timezone.now()
        app.save()
        return Response(LoanDetailSerializer(loan).data, status=status.HTTP_201_CREATED)


class LoanViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsTenantUser]
    filterset_fields = ['status', 'borrower']
    search_fields = ['borrower__email']
    ordering_fields = ['created_at', 'outstanding_principal', 'days_past_due']

    def get_queryset(self):
        qs = Loan.objects.filter(institution=self.request.user.institution).select_related('borrower__profile', 'product')
        if self.request.user.role == 'borrower' and hasattr(self.request.user, 'borrower_profile'):
            qs = qs.filter(borrower=self.request.user.borrower_profile)
        return qs

    def get_serializer_class(self):
        if self.action == 'list':
            return LoanListSerializer
        return LoanDetailSerializer
