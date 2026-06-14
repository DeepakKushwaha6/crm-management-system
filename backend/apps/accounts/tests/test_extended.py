import pytest
from apps.notifications.models import Notification
from apps.accounts.models import AuditLog


@pytest.mark.django_db
class TestNotifications:
    def test_list_notifications(self, authenticated_client, organization, user):
        Notification.objects.create(
            organization=organization, user=user,
            title='Test', message='Hello', notification_type='info',
        )
        response = authenticated_client.get('/api/v1/notifications/')
        assert response.status_code == 200
        assert response.data['count'] >= 1

    def test_mark_read(self, authenticated_client, organization, user):
        n = Notification.objects.create(
            organization=organization, user=user,
            title='Test', message='Hello',
        )
        response = authenticated_client.patch(f'/api/v1/notifications/{n.id}/read/')
        assert response.status_code == 200
        n.refresh_from_db()
        assert n.is_read

    def test_read_all(self, authenticated_client, organization, user):
        Notification.objects.create(
            organization=organization, user=user,
            title='Test', message='Hello',
        )
        response = authenticated_client.post('/api/v1/notifications/read-all/')
        assert response.status_code == 200
        assert response.data['marked_read'] >= 1


@pytest.mark.django_db
class TestOrganizations:
    def test_list_organizations(self, authenticated_client, organization):
        response = authenticated_client.get('/api/v1/organizations/')
        assert response.status_code == 200
        assert len(response.data) >= 1

    def test_organization_detail(self, authenticated_client, organization):
        response = authenticated_client.get(f'/api/v1/organizations/{organization.id}/')
        assert response.status_code == 200
        assert response.data['name'] == organization.name

    def test_list_members(self, authenticated_client, organization, membership):
        response = authenticated_client.get(f'/api/v1/organizations/{organization.id}/members/')
        assert response.status_code == 200
        assert len(response.data) >= 1


@pytest.mark.django_db
class TestAuthExtended:
    def test_logout(self, authenticated_client):
        response = authenticated_client.post('/api/v1/auth/logout/', {'refresh': 'dummy'}, format='json')
        assert response.status_code == 200

    def test_register_duplicate_email(self, api_client, user):
        response = api_client.post('/api/v1/auth/register/', {
            'email': 'test@example.com',
            'password': 'SecurePass123!',
            'first_name': 'Dup',
            'last_name': 'User',
            'organization_name': 'Dup Org',
        }, format='json')
        assert response.status_code == 400


@pytest.mark.django_db
class TestCRMExtended:
    def test_lead_export(self, authenticated_client, organization):
        from apps.crm.models import Lead
        Lead.objects.create(
            organization=organization, first_name='A', last_name='B',
            email='a@b.com', source='web', status='new',
        )
        response = authenticated_client.get('/api/v1/leads/export/')
        assert response.status_code == 200

    def test_customer_activities(self, authenticated_client, organization):
        from apps.crm.models import Customer
        c = Customer.objects.create(
            organization=organization, name='Test', email='t@t.com', status='active',
        )
        response = authenticated_client.get(f'/api/v1/customers/{c.id}/activities/')
        assert response.status_code == 200

    def test_customer_notes(self, authenticated_client, organization):
        from apps.crm.models import Customer
        c = Customer.objects.create(
            organization=organization, name='Test', email='t@t.com', status='active',
        )
        response = authenticated_client.post(
            f'/api/v1/customers/{c.id}/notes/',
            {'subject': 'Note', 'body': 'Test note'},
            format='json',
        )
        assert response.status_code == 201

    def test_team_performance(self, authenticated_client):
        response = authenticated_client.get('/api/v1/analytics/team/')
        assert response.status_code == 200

    def test_departments(self, authenticated_client, organization):
        response = authenticated_client.post('/api/v1/departments/', {
            'name': 'Marketing', 'description': 'Marketing dept',
        }, format='json')
        assert response.status_code == 201

    def test_teams(self, authenticated_client, organization):
        response = authenticated_client.post('/api/v1/teams/', {
            'name': 'Inside Sales', 'description': 'Inside sales team',
        }, format='json')
        assert response.status_code == 201
