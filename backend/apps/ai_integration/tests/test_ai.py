import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'ai'))


@pytest.mark.django_db
class TestAI:
    def test_lead_score(self, authenticated_client):
        response = authenticated_client.post('/api/v1/ai/lead-score/', {
            'features': {
                'source': 'referral', 'status': 'qualified',
                'has_email': True, 'has_phone': True, 'has_company': True,
            },
        }, format='json')
        assert response.status_code == 200
        assert 'score' in response.data
        assert 0 <= response.data['score'] <= 100

    def test_churn_predict(self, authenticated_client):
        response = authenticated_client.post('/api/v1/ai/churn-predict/', {
            'features': {'lifetime_value': 5000, 'status': 'active', 'opportunity_count': 3},
        }, format='json')
        assert response.status_code == 200
        assert 'churn_risk' in response.data

    def test_revenue_forecast(self, authenticated_client):
        response = authenticated_client.post('/api/v1/ai/revenue-forecast/', {
            'period': 'monthly',
        }, format='json')
        assert response.status_code == 200
        assert 'forecasts' in response.data

    def test_follow_up(self, authenticated_client):
        response = authenticated_client.post('/api/v1/ai/follow-up/', {
            'entity_type': 'lead', 'status': 'qualified', 'score': 85,
        }, format='json')
        assert response.status_code == 200
        assert 'recommended_action' in response.data

    def test_generate_email(self, authenticated_client):
        response = authenticated_client.post('/api/v1/ai/generate-email/', {
            'type': 'follow_up',
            'context': {'name': 'John', 'sender': 'Sales'},
        }, format='json')
        assert response.status_code == 200
        assert 'subject' in response.data
        assert 'body' in response.data

    def test_sentiment(self, authenticated_client):
        response = authenticated_client.post('/api/v1/ai/sentiment/', {
            'text': 'Great product, very happy with the service!',
        }, format='json')
        assert response.status_code == 200
        assert response.data['sentiment'] == 'positive'
