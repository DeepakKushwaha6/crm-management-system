import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'ai'))

from services.lead_scoring import score_lead
from services.churn_prediction import predict_churn
from services.revenue_forecast import forecast_revenue
from services.sentiment import analyze_sentiment
from services.email_generator import generate_email
from services.follow_up import recommend_follow_up


class TestLeadScoring:
    def test_hot_lead(self):
        result = score_lead({
            'source': 'referral', 'status': 'qualified',
            'has_email': True, 'has_phone': True, 'has_company': True,
        })
        assert result['score'] >= 60
        assert result['quality'] in ['hot', 'warm']

    def test_cold_lead(self):
        result = score_lead({
            'source': 'cold_call', 'status': 'new',
            'has_email': False, 'has_phone': False, 'has_company': False,
        })
        assert result['score'] < 60


class TestChurnPrediction:
    def test_high_risk(self):
        result = predict_churn({
            'lifetime_value': 500, 'status': 'inactive',
            'opportunity_count': 0, 'won_deals': 0,
        })
        assert result['churn_risk'] >= 0.5

    def test_low_risk(self):
        result = predict_churn({
            'lifetime_value': 50000, 'status': 'active',
            'opportunity_count': 5, 'won_deals': 3,
        })
        assert result['churn_risk'] < 0.5


class TestRevenueForecast:
    def test_monthly_forecast(self):
        result = forecast_revenue([10000, 12000, 15000], 50000, 'monthly')
        assert len(result['forecasts']) == 3


class TestSentiment:
    def test_positive(self):
        assert analyze_sentiment('Great excellent happy service')['sentiment'] == 'positive'

    def test_negative(self):
        assert analyze_sentiment('Terrible awful disappointed service')['sentiment'] == 'negative'


class TestEmailGenerator:
    def test_follow_up_email(self):
        result = generate_email('follow_up', {'name': 'John'})
        assert 'subject' in result
        assert 'John' in result['body'] or 'Valued Customer' in result['body']


class TestFollowUp:
    def test_recommendation(self):
        result = recommend_follow_up({'status': 'qualified', 'score': 90})
        assert 'recommended_action' in result
