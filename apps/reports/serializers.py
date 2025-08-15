from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'
        read_only_fields = ['id', 'institution', 'status', 'file', 'file_size', 'generated_by', 'generated_at', 'created_at']

class GenerateReportSerializer(serializers.Serializer):
    report_type = serializers.ChoiceField(choices=['portfolio_summary', 'collections', 'financial', 'pipeline', 'investor', 'compliance'])
    format = serializers.ChoiceField(choices=['pdf', 'csv', 'excel'], default='pdf')
    parameters = serializers.JSONField(required=False, default=dict)
