from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed database with demo data'

    def handle(self, *args, **options):
        from apps.accounts.models import Organization, OrganizationMembership, Department, Team
        from apps.crm.models import Lead, Customer, Opportunity, Task, Activity, CalendarEvent
        from apps.notifications.models import Notification

        admin, created = User.objects.get_or_create(
            email='admin@crmaipro.com',
            defaults={'first_name': 'Super', 'last_name': 'Admin', 'is_staff': True, 'is_superuser': True},
        )
        if created:
            admin.set_password('Admin123!')
            admin.save()

        org, _ = Organization.objects.get_or_create(
            slug='demo-corp',
            defaults={'name': 'Demo Corporation', 'plan': 'enterprise', 'industry': 'Technology'},
        )

        demo_user, created = User.objects.get_or_create(
            email='demo@crmaipro.com',
            defaults={'first_name': 'Demo', 'last_name': 'User'},
        )
        if created:
            demo_user.set_password('Demo123!')
            demo_user.save()

        OrganizationMembership.objects.get_or_create(
            user=demo_user, organization=org, defaults={'role': 'org_admin'},
        )

        dept, _ = Department.objects.get_or_create(
            organization=org, name='Sales', defaults={'description': 'Sales Department'},
        )
        team, _ = Team.objects.get_or_create(
            organization=org, name='Enterprise Sales', defaults={'department': dept},
        )

        sources = ['web', 'referral', 'cold_call', 'social', 'event']
        statuses = ['new', 'contacted', 'qualified', 'converted', 'lost']
        first_names = ['John', 'Jane', 'Mike', 'Sarah', 'David', 'Emily', 'Chris', 'Lisa']
        companies = ['Acme Corp', 'TechStart', 'GlobalInc', 'DataFlow', 'CloudNine', 'InnovateCo']

        for i in range(50):
            Lead.objects.get_or_create(
                organization=org,
                email=f'lead{i}@example.com',
                defaults={
                    'first_name': random.choice(first_names),
                    'last_name': f'Lead{i}',
                    'phone': f'+1-555-{random.randint(100,999):03d}-{random.randint(1000,9999):04d}',
                    'company': random.choice(companies),
                    'source': random.choice(sources),
                    'status': random.choice(statuses),
                    'score': random.randint(20, 95),
                    'assigned_to': demo_user,
                },
            )

        for i in range(30):
            Customer.objects.get_or_create(
                organization=org,
                email=f'customer{i}@example.com',
                defaults={
                    'name': f'{random.choice(first_names)} Customer{i}',
                    'company': random.choice(companies),
                    'status': random.choice(['active', 'active', 'active', 'inactive']),
                    'lifetime_value': Decimal(str(random.randint(1000, 50000))),
                    'churn_risk': round(random.uniform(0, 0.8), 2),
                    'assigned_to': demo_user,
                },
            )

        stages = ['new', 'contacted', 'qualified', 'proposal', 'negotiation', 'won', 'lost']
        customers = list(Customer.objects.filter(organization=org))
        for i in range(40):
            customer = random.choice(customers) if customers else None
            stage = random.choice(stages)
            opp, created = Opportunity.objects.get_or_create(
                organization=org,
                title=f'Deal #{i+1} - {random.choice(companies)}',
                defaults={
                    'customer': customer,
                    'stage': stage,
                    'amount': Decimal(str(random.randint(5000, 100000))),
                    'probability': random.randint(10, 90),
                    'assigned_to': demo_user,
                    'expected_close_date': (timezone.now() + timedelta(days=random.randint(-30, 90))).date(),
                },
            )
            if created and stage == 'won':
                opp.won_at = timezone.now() - timedelta(days=random.randint(1, 60))
                opp.probability = 100
                opp.save()

        priorities = ['low', 'medium', 'high', 'urgent']
        for i in range(25):
            Task.objects.get_or_create(
                organization=org,
                title=f'Task: Follow up #{i+1}',
                defaults={
                    'description': f'Follow up with prospect #{i+1}',
                    'priority': random.choice(priorities),
                    'status': random.choice(['pending', 'in_progress', 'completed']),
                    'assigned_to': demo_user,
                    'created_by': demo_user,
                    'due_date': timezone.now() + timedelta(days=random.randint(-5, 14)),
                },
            )

        for i in range(20):
            Activity.objects.create(
                organization=org,
                user=demo_user,
                activity_type=random.choice(['call', 'email', 'meeting', 'note']),
                related_type='customer',
                related_id=random.choice(customers).id if customers else org.id,
                subject=f'Activity #{i+1}',
                body=f'Sample activity log entry #{i+1}',
                sentiment=random.choice(['positive', 'neutral', 'negative']),
            )

        Notification.objects.get_or_create(
            organization=org, user=demo_user, title='Welcome to CRM AI PRO',
            defaults={
                'message': 'Your account has been set up successfully.',
                'notification_type': 'success',
            },
        )

        self.stdout.write(self.style.SUCCESS(
            'Seed data created successfully!\n'
            'Admin: admin@crmaipro.com / Admin123!\n'
            'Demo: demo@crmaipro.com / Demo123!'
        ))
