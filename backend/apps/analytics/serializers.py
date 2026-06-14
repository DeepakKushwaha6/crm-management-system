from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = [
            'id', 'name', 'report_type', 'parameters', 'schedule',
            'is_scheduled', 'last_run_at', 'created_by', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'last_run_at', 'created_at', 'updated_at']
