from django.db import models
from django.conf import settings
from core.models import TenantModel


class Report(TenantModel):
    REPORT_TYPES = [
        ('leads', 'Leads Report'),
        ('pipeline', 'Pipeline Report'),
        ('revenue', 'Revenue Report'),
        ('team', 'Team Performance'),
        ('custom', 'Custom Report'),
    ]
    FORMAT_CHOICES = [
        ('pdf', 'PDF'),
        ('excel', 'Excel'),
        ('csv', 'CSV'),
    ]

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
    )
    name = models.CharField(max_length=255)
    report_type = models.CharField(max_length=50, choices=REPORT_TYPES)
    parameters = models.JSONField(default=dict, blank=True)
    schedule = models.CharField(max_length=100, blank=True)
    last_run_at = models.DateTimeField(null=True, blank=True)
    is_scheduled = models.BooleanField(default=False)

    class Meta:
        db_table = 'reports'
        ordering = ['-created_at']
