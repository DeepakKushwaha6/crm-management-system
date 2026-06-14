import pytest
from apps.crm.models import Lead, Customer, Opportunity, Task


@pytest.mark.django_db
class TestLeads:
    def test_create_lead(self, authenticated_client, organization):
        response = authenticated_client.post('/api/v1/leads/', {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'company': 'Acme',
            'source': 'web',
            'status': 'new',
        })
        assert response.status_code == 201
        assert Lead.objects.filter(organization=organization).count() == 1

    def test_list_leads(self, authenticated_client, organization):
        Lead.objects.create(
            organization=organization, first_name='A', last_name='B',
            email='a@b.com', source='web', status='new',
        )
        response = authenticated_client.get('/api/v1/leads/')
        assert response.status_code == 200
        assert response.data['count'] == 1

    def test_bulk_delete(self, authenticated_client, organization):
        lead = Lead.objects.create(
            organization=organization, first_name='A', last_name='B',
            email='a@b.com', source='web', status='new',
        )
        response = authenticated_client.post('/api/v1/leads/bulk/', {
            'ids': [str(lead.id)], 'action': 'delete',
        })
        assert response.status_code == 200
        assert Lead.objects.count() == 0


@pytest.mark.django_db
class TestCustomers:
    def test_create_customer(self, authenticated_client, organization):
        response = authenticated_client.post('/api/v1/customers/', {
            'name': 'Test Customer',
            'email': 'cust@example.com',
            'status': 'active',
        })
        assert response.status_code == 201


@pytest.mark.django_db
class TestOpportunities:
    def test_create_opportunity(self, authenticated_client, organization, user):
        response = authenticated_client.post('/api/v1/opportunities/', {
            'title': 'Big Deal',
            'stage': 'new',
            'amount': '50000.00',
            'probability': 25,
            'assigned_to': str(user.id),
        })
        assert response.status_code == 201

    def test_pipeline(self, authenticated_client, organization):
        Opportunity.objects.create(
            organization=organization, title='Deal 1',
            stage='new', amount=10000,
        )
        response = authenticated_client.get('/api/v1/opportunities/pipeline/')
        assert response.status_code == 200
        assert 'new' in response.data

    def test_update_stage(self, authenticated_client, organization):
        opp = Opportunity.objects.create(
            organization=organization, title='Deal', stage='new', amount=5000,
        )
        response = authenticated_client.patch(f'/api/v1/opportunities/{opp.id}/stage/', {
            'stage': 'won',
        })
        assert response.status_code == 200
        opp.refresh_from_db()
        assert opp.stage == 'won'


@pytest.mark.django_db
class TestTasks:
    def test_create_task(self, authenticated_client, organization, user):
        response = authenticated_client.post('/api/v1/tasks/', {
            'title': 'Follow up',
            'priority': 'high',
            'status': 'pending',
            'assigned_to': str(user.id),
        })
        assert response.status_code == 201
