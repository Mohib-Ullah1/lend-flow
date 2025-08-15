from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.core.permissions import IsTenantUser
from .models import Borrower
from .serializers import BorrowerListSerializer, BorrowerDetailSerializer, BorrowerCreateSerializer

class BorrowerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsTenantUser]

    def get_queryset(self):
        return Borrower.objects.filter(institution=self.request.user.institution).select_related('profile')

    def get_serializer_class(self):
        if self.action == 'list':
            return BorrowerListSerializer
        if self.action == 'create':
            return BorrowerCreateSerializer
        return BorrowerDetailSerializer

    @action(detail=True, methods=['post'])
    def verify_kyc(self, request, pk=None):
        borrower = self.get_object()
        borrower.kyc_status = 'verified'
        borrower.save(update_fields=['kyc_status'])
        return Response({'status': 'verified'})

    @action(detail=True, methods=['post'])
    def blacklist(self, request, pk=None):
        borrower = self.get_object()
        borrower.is_blacklisted = True
        borrower.save(update_fields=['is_blacklisted'])
        return Response({'status': 'blacklisted'})
