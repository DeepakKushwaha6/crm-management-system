from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView, LoginView, LogoutView, MeView,
    OrganizationViewSet, DepartmentViewSet, TeamViewSet, AuditLogViewSet,
)

router = DefaultRouter()
router.register('organizations', OrganizationViewSet, basename='organization')
router.register('departments', DepartmentViewSet, basename='department')
router.register('teams', TeamViewSet, basename='team')
router.register('audit-logs', AuditLogViewSet, basename='audit-log')

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/me/', MeView.as_view(), name='me'),
    path('', include(router.urls)),
]
