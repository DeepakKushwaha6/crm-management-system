from django.urls import path
from .views import (
    LeadScoreView, ChurnPredictView, RevenueForecastView,
    FollowUpRecommendationView, EmailGeneratorView, SentimentAnalysisView,
)

urlpatterns = [
    path('ai/lead-score/', LeadScoreView.as_view(), name='ai-lead-score'),
    path('ai/churn-predict/', ChurnPredictView.as_view(), name='ai-churn-predict'),
    path('ai/revenue-forecast/', RevenueForecastView.as_view(), name='ai-revenue-forecast'),
    path('ai/follow-up/', FollowUpRecommendationView.as_view(), name='ai-follow-up'),
    path('ai/generate-email/', EmailGeneratorView.as_view(), name='ai-generate-email'),
    path('ai/sentiment/', SentimentAnalysisView.as_view(), name='ai-sentiment'),
]
