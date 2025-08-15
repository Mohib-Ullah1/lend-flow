from rest_framework import viewsets, status, parsers
from rest_framework.response import Response
from apps.core.permissions import IsTenantUser
from .models import Document
from .serializers import DocumentSerializer, DocumentUploadSerializer

class DocumentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsTenantUser]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]

    def get_queryset(self):
        qs = Document.objects.filter(institution=self.request.user.institution)
        borrower_id = self.request.query_params.get('borrower_id')
        if borrower_id:
            qs = qs.filter(borrower_id=borrower_id)
        return qs

    def get_serializer_class(self):
        if self.action == 'create':
            return DocumentUploadSerializer
        return DocumentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        doc = serializer.save()
        return Response(DocumentSerializer(doc).data, status=status.HTTP_201_CREATED)
