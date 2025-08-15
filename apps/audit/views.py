from rest_framework import viewsets
from rest_framework import serializers as drf_serializers
from apps.core.permissions import IsAdminOrReadOnly
from .models import AuditLog

class AuditLogSerializer(drf_serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'

class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AuditLogSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ['action', 'resource_type', 'username']
    ordering_fields = ['timestamp']

    def get_queryset(self):
        qs = AuditLog.objects.all()
        if hasattr(self.request.user, 'institution_id') and self.request.user.institution_id:
            qs = qs.filter(institution_id=self.request.user.institution_id)
        return qs
