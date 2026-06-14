import csv
import io
from rest_framework import serializers
from apps.accounts.serializers import UserSerializer
from .models import Lead, Customer, Opportunity, Task, Activity, Document, CalendarEvent


class LeadSerializer(serializers.ModelSerializer):
    assigned_to_detail = UserSerializer(source='assigned_to', read_only=True)
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Lead
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'email', 'phone',
            'company', 'title', 'source', 'status', 'score', 'notes',
            'assigned_to', 'assigned_to_detail', 'custom_fields',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'score', 'created_at', 'updated_at']


class CustomerSerializer(serializers.ModelSerializer):
    assigned_to_detail = UserSerializer(source='assigned_to', read_only=True)

    class Meta:
        model = Customer
        fields = [
            'id', 'name', 'email', 'phone', 'company', 'status',
            'churn_risk', 'lifetime_value', 'address', 'notes',
            'assigned_to', 'assigned_to_detail', 'custom_fields',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'churn_risk', 'created_at', 'updated_at']


class OpportunitySerializer(serializers.ModelSerializer):
    assigned_to_detail = UserSerializer(source='assigned_to', read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)

    class Meta:
        model = Opportunity
        fields = [
            'id', 'title', 'description', 'stage', 'amount', 'probability',
            'expected_close_date', 'won_at', 'lost_at', 'lost_reason',
            'customer', 'customer_name', 'lead', 'assigned_to', 'assigned_to_detail',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'won_at', 'lost_at', 'created_at', 'updated_at']


class TaskSerializer(serializers.ModelSerializer):
    assigned_to_detail = UserSerializer(source='assigned_to', read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'priority', 'status',
            'due_date', 'reminder_at', 'completed_at',
            'assigned_to', 'assigned_to_detail', 'created_by',
            'related_type', 'related_id', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'completed_at', 'created_at', 'updated_at']


class ActivitySerializer(serializers.ModelSerializer):
    user_detail = UserSerializer(source='user', read_only=True)

    class Meta:
        model = Activity
        fields = [
            'id', 'activity_type', 'related_type', 'related_id',
            'subject', 'body', 'sentiment', 'metadata',
            'user', 'user_detail', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'name', 'file', 'file_type', 'file_size', 'customer', 'created_at']
        read_only_fields = ['id', 'file_type', 'file_size', 'created_at']


class CalendarEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarEvent
        fields = [
            'id', 'title', 'description', 'event_type',
            'start_time', 'end_time', 'location',
            'related_type', 'related_id', 'is_all_day', 'user',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class BulkLeadActionSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.UUIDField())
    action = serializers.ChoiceField(choices=['delete', 'assign', 'update_status'])
    assigned_to = serializers.UUIDField(required=False)
    status = serializers.CharField(required=False)


class CSVImportSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError('File must be a CSV.')
        return value
