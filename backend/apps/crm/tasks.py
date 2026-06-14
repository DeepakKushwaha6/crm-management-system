from celery import shared_task
from django.utils import timezone


@shared_task
def score_all_leads(organization_id):
    from apps.crm.models import Lead
    from apps.accounts.models import Organization
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'ai'))
    from services.lead_scoring import score_lead

    org = Organization.objects.get(id=organization_id)
    leads = Lead.objects.filter(organization=org)
    updated = 0
    for lead in leads:
        features = {
            'source': lead.source, 'status': lead.status,
            'has_email': bool(lead.email), 'has_phone': bool(lead.phone),
            'has_company': bool(lead.company),
        }
        result = score_lead(features)
        lead.score = result['score']
        lead.save(update_fields=['score'])
        updated += 1
    return {'scored': updated}


@shared_task
def send_task_reminders():
    from apps.crm.models import Task
    from apps.notifications.models import Notification
    from datetime import timedelta

    now = timezone.now()
    upcoming = Task.objects.filter(
        status='pending',
        reminder_at__lte=now,
        reminder_at__gte=now - timedelta(hours=1),
    )
    for task in upcoming:
        Notification.objects.create(
            organization=task.organization,
            user=task.assigned_to,
            title='Task Reminder',
            message=f'Task due: {task.title}',
            notification_type='task',
            link=f'/dashboard/tasks/{task.id}',
        )
    return {'reminders_sent': upcoming.count()}


@shared_task
def run_scheduled_reports():
    from apps.analytics.models import Report

    reports = Report.objects.filter(is_scheduled=True)
    for report in reports:
        report.last_run_at = timezone.now()
        report.save(update_fields=['last_run_at'])
    return {'reports_run': reports.count()}
