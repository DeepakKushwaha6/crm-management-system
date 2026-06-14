import pytest


@pytest.mark.django_db
class TestDashboard:
    def test_dashboard(self, authenticated_client, organization):
        response = authenticated_client.get('/api/v1/dashboard/')
        assert response.status_code == 200
        assert 'revenue' in response.data
        assert 'sales' in response.data

    def test_revenue_analytics(self, authenticated_client):
        response = authenticated_client.get('/api/v1/analytics/revenue/')
        assert response.status_code == 200

    def test_pipeline_analytics(self, authenticated_client):
        response = authenticated_client.get('/api/v1/analytics/pipeline/')
        assert response.status_code == 200


@pytest.mark.django_db
class TestReports:
    def test_create_report(self, authenticated_client, user):
        response = authenticated_client.post('/api/v1/reports/', {
            'name': 'Monthly Leads',
            'report_type': 'leads',
        })
        assert response.status_code == 201
