import io
import pytest
from django.utils import timezone
from apps.crm.models import Lead, Customer, Opportunity
from apps.analytics.models import Report


@pytest.mark.django_db
class TestLeadImportExport:
    def test_import_csv(self, authenticated_client, organization):
        csv_content = "first_name,last_name,email,phone,company,source,status\nJohn,Doe,john@test.com,555-1234,Acme,web,new\n"
        csv_file = io.BytesIO(csv_content.encode('utf-8'))
        csv_file.name = 'leads.csv'
        response = authenticated_client.post(
            '/api/v1/leads/import/',
            {'file': csv_file},
            format='multipart',
        )
        assert response.status_code == 200
        assert response.data['imported'] == 1

    def test_bulk_assign(self, authenticated_client, organization, user):
        lead = Lead.objects.create(
            organization=organization, first_name='A', last_name='B',
            email='bulk@test.com', source='web', status='new',
        )
        response = authenticated_client.post('/api/v1/leads/bulk/', {
            'ids': [str(lead.id)], 'action': 'assign', 'assigned_to': str(user.id),
        }, format='json')
        assert response.status_code == 200
        lead.refresh_from_db()
        assert lead.assigned_to == user

    def test_bulk_update_status(self, authenticated_client, organization):
        lead = Lead.objects.create(
            organization=organization, first_name='A', last_name='B',
            email='status@test.com', source='web', status='new',
        )
        response = authenticated_client.post('/api/v1/leads/bulk/', {
            'ids': [str(lead.id)], 'action': 'update_status', 'status': 'contacted',
        }, format='json')
        assert response.status_code == 200
        lead.refresh_from_db()
        assert lead.status == 'contacted'

    def test_score_lead_by_id(self, authenticated_client, organization):
        lead = Lead.objects.create(
            organization=organization, first_name='Score', last_name='Test',
            email='score@test.com', company='Acme', source='referral', status='qualified',
        )
        response = authenticated_client.post('/api/v1/ai/lead-score/', {
            'lead_id': str(lead.id),
        }, format='json')
        assert response.status_code == 200
        assert 'score' in response.data

    def test_churn_by_customer_id(self, authenticated_client, organization):
        customer = Customer.objects.create(
            organization=organization, name='Churn Test',
            email='churn@test.com', status='active', lifetime_value=5000,
        )
        Opportunity.objects.create(
            organization=organization, customer=customer,
            title='Deal', stage='won', amount=10000,
        )
        response = authenticated_client.post('/api/v1/ai/churn-predict/', {
            'customer_id': str(customer.id),
        }, format='json')
        assert response.status_code == 200
        assert 'churn_risk' in response.data



@pytest.mark.django_db
class TestOpportunityStages:
    def test_lost_stage(self, authenticated_client, organization):
        opp = Opportunity.objects.create(
            organization=organization, title='Lost Deal', stage='negotiation', amount=5000,
        )
        response = authenticated_client.patch(f'/api/v1/opportunities/{opp.id}/stage/', {
            'stage': 'lost', 'lost_reason': 'Budget constraints',
        }, format='json')
        assert response.status_code == 200
        opp.refresh_from_db()
        assert opp.stage == 'lost'
        assert opp.lost_reason == 'Budget constraints'

    def test_invalid_stage(self, authenticated_client, organization):
        opp = Opportunity.objects.create(
            organization=organization, title='Deal', stage='new', amount=1000,
        )
        response = authenticated_client.patch(f'/api/v1/opportunities/{opp.id}/stage/', {
            'stage': 'invalid_stage',
        }, format='json')
        assert response.status_code == 400


@pytest.mark.django_db
class TestActivitiesAndTasks:
    def test_create_activity(self, authenticated_client, organization):
        customer = Customer.objects.create(
            organization=organization, name='Act Test', email='act@test.com', status='active',
        )
        response = authenticated_client.post('/api/v1/activities/', {
            'activity_type': 'call',
            'related_type': 'customer',
            'related_id': str(customer.id),
            'subject': 'Follow up call',
            'body': 'Discussed pricing',
        }, format='json')
        assert response.status_code == 201

    def test_update_profile(self, authenticated_client, user):
        response = authenticated_client.patch('/api/v1/auth/me/', {
            'first_name': 'Updated',
        }, format='json')
        assert response.status_code == 200
        assert response.data['first_name'] == 'Updated'

    def test_invite_member(self, authenticated_client, organization):
        response = authenticated_client.post(
            f'/api/v1/organizations/{organization.id}/members/',
            {
                'email': 'newmember@test.com',
                'first_name': 'New',
                'last_name': 'Member',
                'role': 'sales_executive',
            },
            format='json',
        )
        assert response.status_code == 201

    def test_sentiment_empty_text(self, authenticated_client):
        response = authenticated_client.post('/api/v1/ai/sentiment/', {'text': ''}, format='json')
        assert response.status_code == 400

    def test_lead_not_found(self, authenticated_client):
        response = authenticated_client.post('/api/v1/ai/lead-score/', {
            'lead_id': '00000000-0000-0000-0000-000000000000',
        }, format='json')
        assert response.status_code == 404
