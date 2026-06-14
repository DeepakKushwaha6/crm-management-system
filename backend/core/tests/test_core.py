import pytest
from django.test import RequestFactory
from apps.accounts.models import OrganizationMembership
from core.middleware import TenantMiddleware, AuditMiddleware, SecurityHeadersMiddleware
from core.authentication import TenantJWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
class TestMiddleware:
    def test_tenant_middleware_sets_context(self, user, organization, membership):
        factory = RequestFactory()
        request = factory.get('/', HTTP_X_ORGANIZATION_ID=str(organization.id))
        request.user = user

        middleware = TenantMiddleware(lambda r: None)
        middleware.process_request(request)

        from core.thread_locals import get_current_organization
        assert get_current_organization() == organization

    def test_audit_middleware(self, user):
        factory = RequestFactory()
        request = factory.get('/', REMOTE_ADDR='127.0.0.1', HTTP_USER_AGENT='TestAgent')
        request.user = user

        middleware = AuditMiddleware(lambda r: None)
        middleware.process_request(request)
        assert request.audit_data['ip_address'] == '127.0.0.1'

    def test_security_headers(self):
        factory = RequestFactory()
        request = factory.get('/')

        def get_response(req):
            from django.http import HttpResponse
            return HttpResponse('ok')

        middleware = SecurityHeadersMiddleware(get_response)
        response = middleware(request)
        assert response['X-Content-Type-Options'] == 'nosniff'
        assert response['X-Frame-Options'] == 'DENY'


@pytest.mark.django_db
class TestAuthentication:
    def test_tenant_jwt_fallback_membership(self, user, organization, membership):
        factory = RequestFactory()
        refresh = RefreshToken.for_user(user)
        request = factory.get('/', HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        auth = TenantJWTAuthentication()
        result = auth.authenticate(request)
        assert result is not None
        assert result[0] == user

    def test_tenant_jwt_with_org_header(self, user, organization, membership):
        factory = RequestFactory()
        refresh = RefreshToken.for_user(user)
        request = factory.get(
            '/',
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}',
            HTTP_X_ORGANIZATION_ID=str(organization.id),
        )

        auth = TenantJWTAuthentication()
        result = auth.authenticate(request)
        assert result is not None
        assert hasattr(request, 'organization')


@pytest.mark.django_db
class TestCalendarAndDocuments:
    def test_create_calendar_event(self, authenticated_client, user):
        from django.utils import timezone
        from datetime import timedelta
        now = timezone.now()
        response = authenticated_client.post('/api/v1/calendar/', {
            'title': 'Team Meeting',
            'event_type': 'meeting',
            'start_time': now.isoformat(),
            'end_time': (now + timedelta(hours=1)).isoformat(),
            'user': str(user.id),
        }, format='json')
        assert response.status_code == 201

    def test_list_calendar(self, authenticated_client):
        response = authenticated_client.get('/api/v1/calendar/')
        assert response.status_code == 200

    def test_audit_logs(self, authenticated_client):
        response = authenticated_client.get('/api/v1/audit-logs/')
        assert response.status_code == 200

    def test_update_organization(self, authenticated_client, organization):
        response = authenticated_client.patch(
            f'/api/v1/organizations/{organization.id}/',
            {'industry': 'Technology'},
            format='json',
        )
        assert response.status_code == 200

    def test_revenue_analytics_weekly(self, authenticated_client):
        response = authenticated_client.get('/api/v1/analytics/revenue/?period=weekly')
        assert response.status_code == 200
