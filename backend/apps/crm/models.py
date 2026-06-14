from django.db import models
from django.conf import settings
from core.models import TenantModel


class Lead(TenantModel):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('converted', 'Converted'),
        ('lost', 'Lost'),
    ]
    SOURCE_CHOICES = [
        ('web', 'Website'),
        ('referral', 'Referral'),
        ('cold_call', 'Cold Call'),
        ('social', 'Social Media'),
        ('event', 'Event'),
        ('other', 'Other'),
    ]

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='assigned_leads',
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=100, blank=True)
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES, default='web')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='new')
    score = models.IntegerField(default=0)
    notes = models.TextField(blank=True)
    custom_fields = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'leads'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['organization', 'status']),
            models.Index(fields=['organization', 'assigned_to']),
        ]

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'.strip()


class Customer(TenantModel):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('churned', 'Churned'),
    ]

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='assigned_customers',
    )
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='active')
    churn_risk = models.FloatField(default=0.0)
    lifetime_value = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    address = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    custom_fields = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'customers'
        ordering = ['-created_at']


class Opportunity(TenantModel):
    STAGE_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('proposal', 'Proposal'),
        ('negotiation', 'Negotiation'),
        ('won', 'Won'),
        ('lost', 'Lost'),
    ]

    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='opportunities',
    )
    lead = models.ForeignKey(
        Lead, on_delete=models.SET_NULL, null=True, blank=True, related_name='opportunities',
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='assigned_opportunities',
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    stage = models.CharField(max_length=50, choices=STAGE_CHOICES, default='new')
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    probability = models.IntegerField(default=10)
    expected_close_date = models.DateField(null=True, blank=True)
    won_at = models.DateTimeField(null=True, blank=True)
    lost_at = models.DateTimeField(null=True, blank=True)
    lost_reason = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'opportunities'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['organization', 'stage']),
            models.Index(fields=['organization', 'expected_close_date']),
        ]


class Task(TenantModel):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assigned_tasks',
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, related_name='created_tasks',
    )
    related_type = models.CharField(max_length=50, blank=True)
    related_id = models.UUIDField(null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    due_date = models.DateTimeField(null=True, blank=True)
    reminder_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'tasks'
        ordering = ['due_date', '-created_at']
        indexes = [
            models.Index(fields=['organization', 'assigned_to', 'due_date']),
        ]


class Activity(TenantModel):
    TYPE_CHOICES = [
        ('call', 'Call'),
        ('email', 'Email'),
        ('meeting', 'Meeting'),
        ('note', 'Note'),
        ('task', 'Task'),
        ('status_change', 'Status Change'),
    ]
    SENTIMENT_CHOICES = [
        ('positive', 'Positive'),
        ('neutral', 'Neutral'),
        ('negative', 'Negative'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, related_name='activities',
    )
    activity_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    related_type = models.CharField(max_length=50)
    related_id = models.UUIDField()
    subject = models.CharField(max_length=255, blank=True)
    body = models.TextField(blank=True)
    sentiment = models.CharField(max_length=20, choices=SENTIMENT_CHOICES, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'activities'
        ordering = ['-created_at']


class Document(TenantModel):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, null=True, blank=True, related_name='documents',
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
    )
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    file_type = models.CharField(max_length=50, blank=True)
    file_size = models.IntegerField(default=0)

    class Meta:
        db_table = 'documents'


class CalendarEvent(TenantModel):
    EVENT_TYPES = [
        ('meeting', 'Meeting'),
        ('call', 'Call'),
        ('follow_up', 'Follow Up'),
        ('task', 'Task'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='calendar_events',
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES, default='meeting')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True)
    related_type = models.CharField(max_length=50, blank=True)
    related_id = models.UUIDField(null=True, blank=True)
    is_all_day = models.BooleanField(default=False)

    class Meta:
        db_table = 'calendar_events'
        ordering = ['start_time']
