from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DashboardView, RevenueAnalyticsView, PipelineAnalyticsView,
    TeamPerformanceView, ReportViewSet,
)

router = DefaultRouter()
router.register('reports', ReportViewSet, basename='report')

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('analytics/revenue/', RevenueAnalyticsView.as_view(), name='revenue-analytics'),
    path('analytics/pipeline/', PipelineAnalyticsView.as_view(), name='pipeline-analytics'),
    path('analytics/team/', TeamPerformanceView.as_view(), name='team-analytics'),
    path('', include(router.urls)),
]
