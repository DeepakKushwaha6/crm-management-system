from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LeadViewSet, CustomerViewSet, OpportunityViewSet,
    TaskViewSet, ActivityViewSet, DocumentViewSet, CalendarViewSet,
)

router = DefaultRouter()
router.register('leads', LeadViewSet, basename='lead')
router.register('customers', CustomerViewSet, basename='customer')
router.register('opportunities', OpportunityViewSet, basename='opportunity')
router.register('tasks', TaskViewSet, basename='task')
router.register('activities', ActivityViewSet, basename='activity')
router.register('documents', DocumentViewSet, basename='document')
router.register('calendar', CalendarViewSet, basename='calendar')

urlpatterns = [
    path('', include(router.urls)),
]
