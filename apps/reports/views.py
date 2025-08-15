from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from apps.core.permissions import IsTenantUser
from .models import Report
from .serializers import ReportSerializer, GenerateReportSerializer

class ReportViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ReportSerializer
    permission_classes = [IsTenantUser]

    def get_queryset(self):
        return Report.objects.filter(institution=self.request.user.institution)

class GenerateReportView(APIView):
    permission_classes = [IsTenantUser]

    def post(self, request):
        serializer = GenerateReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        report_type = serializer.validated_data['report_type']
        name_map = {
            'portfolio_summary': 'Portfolio Summary',
            'collections': 'Collections Report',
            'financial': 'Financial Statement',
            'pipeline': 'Application Pipeline',
            'investor': 'Investor Report',
            'compliance': 'Compliance Report',
        }

        report = Report.objects.create(
            institution=request.user.institution,
            name=f'{name_map.get(report_type, report_type)} — {timezone.now().strftime("%B %Y")}',
            report_type=report_type,
            format=serializer.validated_data['format'],
            parameters=serializer.validated_data.get('parameters', {}),
            status='completed',
            generated_by=request.user,
            generated_at=timezone.now(),
        )

        return Response(ReportSerializer(report).data, status=status.HTTP_201_CREATED)
