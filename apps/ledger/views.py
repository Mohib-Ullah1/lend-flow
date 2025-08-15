from rest_framework import viewsets
from apps.core.permissions import IsTenantUser
from .models import GLAccount, JournalEntry
from .serializers import GLAccountSerializer, JournalEntrySerializer

class GLAccountViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GLAccountSerializer
    queryset = GLAccount.objects.filter(is_active=True)
    permission_classes = [IsTenantUser]

class JournalEntryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = JournalEntrySerializer
    permission_classes = [IsTenantUser]
    filterset_fields = ['reference_type', 'entry_date']
    ordering_fields = ['entry_date', 'created_at']

    def get_queryset(self):
        return JournalEntry.objects.filter(institution=self.request.user.institution).prefetch_related('lines__account')
