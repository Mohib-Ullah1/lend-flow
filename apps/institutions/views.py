from rest_framework import viewsets
from apps.core.permissions import IsAdminOrReadOnly
from .models import Institution
from .serializers import InstitutionSerializer, InstitutionListSerializer

class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'list':
            return InstitutionListSerializer
        return InstitutionSerializer

    def get_queryset(self):
        if self.request.user.role == 'super_admin':
            return Institution.objects.all()
        if self.request.user.institution:
            return Institution.objects.filter(id=self.request.user.institution_id)
        return Institution.objects.none()
