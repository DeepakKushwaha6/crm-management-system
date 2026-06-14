import csv
import io
from datetime import datetime
from django.utils import timezone
from django.db.models import Sum, Count, Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters import rest_framework as filters

from core.permissions import CanWriteCRM, IsReadOnlyOrAbove
from core.thread_locals import get_current_organization
from .models import Lead, Customer, Opportunity, Task, Activity, Document, CalendarEvent
from .serializers import (
    LeadSerializer, CustomerSerializer, OpportunitySerializer,
    TaskSerializer, ActivitySerializer, DocumentSerializer,
    CalendarEventSerializer, BulkLeadActionSerializer, CSVImportSerializer,
)


class TenantViewSetMixin:
    def get_queryset(self):
        org = get_current_organization()
        if not org:
            return self.queryset.model.objects.none()
        return self.queryset.model.objects.filter(organization=org)

    def perform_create(self, serializer):
        serializer.save(organization=get_current_organization())


class LeadFilter(filters.FilterSet):
    status = filters.CharFilter()
    source = filters.CharFilter()
    assigned_to = filters.UUIDFilter()
    min_score = filters.NumberFilter(field_name='score', lookup_expr='gte')

    class Meta:
        model = Lead
        fields = ['status', 'source', 'assigned_to']


class LeadViewSet(TenantViewSetMixin, viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = [IsReadOnlyOrAbove]
    filterset_class = LeadFilter
    search_fields = ['first_name', 'last_name', 'email', 'company']
    ordering_fields = ['created_at', 'score', 'status']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'bulk', 'import_csv']:
            return [CanWriteCRM()]
        return super().get_permissions()

    @action(detail=False, methods=['post'])
    def bulk(self, request):
        serializer = BulkLeadActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        org = get_current_organization()
        leads = Lead.objects.filter(organization=org, id__in=serializer.validated_data['ids'])
        action_type = serializer.validated_data['action']

        if action_type == 'delete':
            count = leads.count()
            leads.delete()
            return Response({'deleted': count})
        elif action_type == 'assign':
            leads.update(assigned_to_id=serializer.validated_data['assigned_to'])
            return Response({'updated': leads.count()})
        elif action_type == 'update_status':
            leads.update(status=serializer.validated_data['status'])
            return Response({'updated': leads.count()})
        return Response({'error': 'Invalid action'}, status=400)

    @action(detail=False, methods=['post'], url_path='import')
    def import_csv(self, request):
        serializer = CSVImportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        org = get_current_organization()
        file = serializer.validated_data['file']
        decoded = file.read().decode('utf-8')
        reader = csv.DictReader(io.StringIO(decoded))
        created = 0
        for row in reader:
            Lead.objects.create(
                organization=org,
                first_name=row.get('first_name', ''),
                last_name=row.get('last_name', ''),
                email=row.get('email', ''),
                phone=row.get('phone', ''),
                company=row.get('company', ''),
                source=row.get('source', 'web'),
                status=row.get('status', 'new'),
            )
            created += 1
        return Response({'imported': created})

    @action(detail=False, methods=['get'])
    def export(self, request):
        org = get_current_organization()
        leads = Lead.objects.filter(organization=org)
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['first_name', 'last_name', 'email', 'phone', 'company', 'source', 'status', 'score'])
        for lead in leads:
            writer.writerow([
                lead.first_name, lead.last_name, lead.email, lead.phone,
                lead.company, lead.source, lead.status, lead.score,
            ])
        return Response(output.getvalue(), content_type='text/csv')


class CustomerViewSet(TenantViewSetMixin, viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsReadOnlyOrAbove]
    search_fields = ['name', 'email', 'company']
    ordering_fields = ['created_at', 'lifetime_value', 'churn_risk']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [CanWriteCRM()]
        return super().get_permissions()

    @action(detail=True, methods=['get'])
    def activities(self, request, pk=None):
        customer = self.get_object()
        activities = Activity.objects.filter(
            organization=customer.organization,
            related_type='customer', related_id=customer.id,
        )
        return Response(ActivitySerializer(activities, many=True).data)

    @action(detail=True, methods=['post'])
    def notes(self, request, pk=None):
        customer = self.get_object()
        activity = Activity.objects.create(
            organization=customer.organization,
            user=request.user,
            activity_type='note',
            related_type='customer',
            related_id=customer.id,
            subject=request.data.get('subject', 'Note'),
            body=request.data.get('body', ''),
        )
        return Response(ActivitySerializer(activity).data, status=201)


class OpportunityFilter(filters.FilterSet):
    stage = filters.CharFilter()
    assigned_to = filters.UUIDFilter()

    class Meta:
        model = Opportunity
        fields = ['stage', 'assigned_to']


class OpportunityViewSet(TenantViewSetMixin, viewsets.ModelViewSet):
    queryset = Opportunity.objects.select_related('customer', 'assigned_to')
    serializer_class = OpportunitySerializer
    permission_classes = [IsReadOnlyOrAbove]
    filterset_class = OpportunityFilter
    search_fields = ['title']
    ordering_fields = ['created_at', 'amount', 'expected_close_date']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'update_stage']:
            return [CanWriteCRM()]
        return super().get_permissions()

    @action(detail=False, methods=['get'])
    def pipeline(self, request):
        org = get_current_organization()
        stages = ['new', 'contacted', 'qualified', 'proposal', 'negotiation', 'won', 'lost']
        pipeline = {}
        for stage in stages:
            opps = Opportunity.objects.filter(organization=org, stage=stage)
            pipeline[stage] = {
                'count': opps.count(),
                'total_amount': float(opps.aggregate(total=Sum('amount'))['total'] or 0),
                'opportunities': OpportunitySerializer(opps[:50], many=True).data,
            }
        return Response(pipeline)

    @action(detail=True, methods=['patch'], url_path='stage')
    def update_stage(self, request, pk=None):
        opp = self.get_object()
        new_stage = request.data.get('stage')
        if new_stage not in dict(Opportunity.STAGE_CHOICES):
            return Response({'error': 'Invalid stage'}, status=400)
        opp.stage = new_stage
        if new_stage == 'won':
            opp.won_at = timezone.now()
            opp.probability = 100
        elif new_stage == 'lost':
            opp.lost_at = timezone.now()
            opp.lost_reason = request.data.get('lost_reason', '')
            opp.probability = 0
        opp.save()
        Activity.objects.create(
            organization=opp.organization,
            user=request.user,
            activity_type='status_change',
            related_type='opportunity',
            related_id=opp.id,
            subject=f'Stage changed to {new_stage}',
        )
        return Response(OpportunitySerializer(opp).data)


class TaskViewSet(TenantViewSetMixin, viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsReadOnlyOrAbove]
    search_fields = ['title']
    ordering_fields = ['due_date', 'priority', 'created_at']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [CanWriteCRM()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(
            organization=get_current_organization(),
            created_by=self.request.user,
        )


class ActivityViewSet(TenantViewSetMixin, viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [CanWriteCRM]
    filterset_fields = ['activity_type', 'related_type', 'related_id']

    def perform_create(self, serializer):
        serializer.save(
            organization=get_current_organization(),
            user=self.request.user,
        )


class DocumentViewSet(TenantViewSetMixin, viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [CanWriteCRM]

    def perform_create(self, serializer):
        file = self.request.FILES.get('file')
        serializer.save(
            organization=get_current_organization(),
            uploaded_by=self.request.user,
            file_size=file.size if file else 0,
            file_type=file.content_type if file else '',
        )


class CalendarViewSet(TenantViewSetMixin, viewsets.ModelViewSet):
    queryset = CalendarEvent.objects.all()
    serializer_class = CalendarEventSerializer
    permission_classes = [IsReadOnlyOrAbove]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [CanWriteCRM()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(
            organization=get_current_organization(),
            user=self.request.user,
        )
