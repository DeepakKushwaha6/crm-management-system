import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestAuth:
    def test_register(self, api_client):
        response = api_client.post('/api/v1/auth/register/', {
            'email': 'new@example.com',
            'password': 'SecurePass123!',
            'first_name': 'New',
            'last_name': 'User',
            'organization_name': 'New Company',
        })
        assert response.status_code == 201
        assert 'tokens' in response.data
        assert response.data['user']['email'] == 'new@example.com'

    def test_login(self, api_client, user, membership):
        response = api_client.post('/api/v1/auth/login/', {
            'email': 'test@example.com',
            'password': 'Test1234!',
        })
        assert response.status_code == 200
        assert 'tokens' in response.data

    def test_login_invalid(self, api_client, user):
        response = api_client.post('/api/v1/auth/login/', {
            'email': 'test@example.com',
            'password': 'wrong',
        })
        assert response.status_code == 401

    def test_me(self, authenticated_client, user):
        response = authenticated_client.get('/api/v1/auth/me/')
        assert response.status_code == 200
        assert response.data['email'] == user.email
