import pytest
from django.contrib.auth import get_user_model
from apps.accounts.models import Organization, OrganizationMembership

User = get_user_model()


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email='test@example.com', password='Test1234!',
        first_name='Test', last_name='User',
    )


@pytest.fixture
def organization(db):
    return Organization.objects.create(name='Test Org', slug='test-org')


@pytest.fixture
def membership(db, user, organization):
    return OrganizationMembership.objects.create(
        user=user, organization=organization, role='org_admin',
    )


@pytest.fixture
def authenticated_client(api_client, user, organization, membership):
    from rest_framework_simplejwt.tokens import RefreshToken
    from core.thread_locals import set_current_organization, set_current_membership

    refresh = RefreshToken.for_user(user)
    api_client.credentials(
        HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}',
        HTTP_X_ORGANIZATION_ID=str(organization.id),
    )
    set_current_organization(organization)
    set_current_membership(membership)

    original_request = api_client.request

    def request_with_tenant(*args, **kwargs):
        set_current_organization(organization)
        set_current_membership(membership)
        return original_request(*args, **kwargs)

    api_client.request = request_with_tenant
    return api_client
