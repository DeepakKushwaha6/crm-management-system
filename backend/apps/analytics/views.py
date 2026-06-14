from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum, Count, Avg, Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from core.permissions import IsReadOnlyOrAbove, CanWriteCRM
from core.thread_locals import get_current_organization
from apps.crm.models import Lead, Customer, Opportunity, Task, Activity
from .models import Report
from .serializers import ReportSerializer
from .export import export_report_pdf, export_report_excel


class DashboardView(APIView):
    permission_classes = [IsReadOnlyOrAbove]

    def get(self, request):
        org = get_current_organization()
        if not org:
            return Response({'error': 'No organization context'}, status=400)

        now = timezone.now()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        leads = Lead.objects.filter(organization=org)
        customers = Customer.objects.filter(organization=org)
        opportunities = Opportunity.objects.filter(organization=org)
        tasks = Task.objects.filter(organization=org)

        won_opps = opportunities.filter(stage='won')
        lost_opps = opportunities.filter(stage='lost')
        open_opps = opportunities.exclude(stage__in=['won', 'lost'])

        total_revenue = won_opps.aggregate(total=Sum('amount'))['total'] or 0
        monthly_revenue = won_opps.filter(won_at__gte=month_start).aggregate(
            total=Sum('amount')
        )['total'] or 0
        pipeline_value = open_opps.aggregate(total=Sum('amount'))['total'] or 0

        total_leads = leads.count()
        converted_leads = leads.filter(status='converted').count()
        conversion_rate = (converted_leads / total_leads * 100) if total_leads else 0

        win_count = won_opps.count()
        loss_count = lost_opps.count()
        win_rate = (win_count / (win_count + loss_count) * 100) if (win_count + loss_count) else 0

        return Response({
            'revenue': {
                'total': float(total_revenue),
                'monthly': float(monthly_revenue),
                'pipeline_value': float(pipeline_value),
            },
            'sales': {
                'total_leads': total_leads,
                'converted_leads': converted_leads,
                'open_opportunities': open_opps.count(),
                'won_deals': win_count,
                'lost_deals': loss_count,
            },
            'conversion': {
                'lead_conversion_rate': round(conversion_rate, 2),
                'win_rate': round(win_rate, 2),
            },
            'customers': {
                'total': customers.count(),
                'active': customers.filter(status='active').count(),
                'at_risk': customers.filter(churn_risk__gte=0.7).count(),
            },
            'tasks': {
                'pending': tasks.filter(status='pending').count(),
                'overdue': tasks.filter(
                    status='pending', due_date__lt=now
                ).count(),
                'completed_this_month': tasks.filter(
                    status='completed', completed_at__gte=month_start
                ).count(),
            },
            'recent_activities': list(
                Activity.objects.filter(organization=org)
                .select_related('user')[:10]
                .values('id', 'activity_type', 'subject', 'created_at', 'user__email')
            ),
        })


class RevenueAnalyticsView(APIView):
    permission_classes = [IsReadOnlyOrAbove]

    def get(self, request):
        org = get_current_organization()
        period = request.query_params.get('period', 'monthly')
        now = timezone.now()

        data = []
        for i in range(12):
            if period == 'weekly':
                start = now - timedelta(weeks=i + 1)
                end = now - timedelta(weeks=i)
                label = start.strftime('%Y-W%W')
            else:
                month = now.month - i
                year = now.year
                while month <= 0:
                    month += 12
                    year -= 1
                start = now.replace(year=year, month=month, day=1)
                if month == 12:
                    end = start.replace(year=year + 1, month=1, day=1)
                else:
                    end = start.replace(month=month + 1, day=1)
                label = start.strftime('%Y-%m')

            revenue = Opportunity.objects.filter(
                organization=org, stage='won',
                won_at__gte=start, won_at__lt=end,
            ).aggregate(total=Sum('amount'))['total'] or 0

            data.append({'period': label, 'revenue': float(revenue)})

        return Response({'data': list(reversed(data))})


class PipelineAnalyticsView(APIView):
    permission_classes = [IsReadOnlyOrAbove]

    def get(self, request):
        org = get_current_organization()
        stages = ['new', 'contacted', 'qualified', 'proposal', 'negotiation', 'won', 'lost']
        funnel = []
        for stage in stages:
            opps = Opportunity.objects.filter(organization=org, stage=stage)
            funnel.append({
                'stage': stage,
                'count': opps.count(),
                'value': float(opps.aggregate(total=Sum('amount'))['total'] or 0),
            })
        return Response({'funnel': funnel})


class TeamPerformanceView(APIView):
    permission_classes = [IsReadOnlyOrAbove]

    def get(self, request):
        org = get_current_organization()
        from apps.accounts.models import OrganizationMembership

        members = OrganizationMembership.objects.filter(
            organization=org, is_active=True
        ).select_related('user')

        performance = []
        for m in members:
            user = m.user
            won = Opportunity.objects.filter(
                organization=org, assigned_to=user, stage='won'
            )
            performance.append({
                'user_id': str(user.id),
                'name': user.full_name,
                'role': m.role,
                'leads_assigned': Lead.objects.filter(organization=org, assigned_to=user).count(),
                'deals_won': won.count(),
                'revenue': float(won.aggregate(total=Sum('amount'))['total'] or 0),
                'tasks_completed': Task.objects.filter(
                    organization=org, assigned_to=user, status='completed'
                ).count(),
            })
        return Response({'team': performance})


class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    permission_classes = [IsReadOnlyOrAbove]

    def get_queryset(self):
        org = get_current_organization()
        if not org:
            return Report.objects.none()
        return Report.objects.filter(organization=org)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [CanWriteCRM()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(
            organization=get_current_organization(),
            created_by=self.request.user,
        )

    @action(detail=True, methods=['get'], url_path='export')
    def export_report(self, request, pk=None):
        report = self.get_object()
        fmt = request.query_params.get('format', 'pdf')
        org = get_current_organization()

        if fmt == 'excel':
            content = export_report_excel(report, org)
            return Response(
                content,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            )
        content = export_report_pdf(report, org)
        return Response(content, content_type='application/pdf')
