from django.utils.deprecation import MiddlewareMixin
from apps.accounts.models import Organization, OrganizationMembership
from .thread_locals import set_current_organization, set_current_membership


class TenantMiddleware(MiddlewareMixin):
    def process_request(self, request):
        set_current_organization(None)
        set_current_membership(None)

        if not request.user.is_authenticated:
            return

        org_id = (
            request.headers.get('X-Organization-ID')
            or request.META.get('HTTP_X_ORGANIZATION_ID')
        )
        if not org_id:
            membership = OrganizationMembership.objects.filter(
                user=request.user
            ).select_related('organization').first()
            if membership:
                set_current_organization(membership.organization)
                set_current_membership(membership)
            return

        try:
            organization = Organization.objects.get(id=org_id)
            membership = OrganizationMembership.objects.get(
                user=request.user, organization=organization
            )
            set_current_organization(organization)
            set_current_membership(membership)
            request.organization = organization
            request.membership = membership
        except (Organization.DoesNotExist, OrganizationMembership.DoesNotExist):
            pass


class AuditMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.audit_data = {
            'ip_address': self._get_client_ip(request),
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
        }

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')


class SecurityHeadersMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        if not response.get('Content-Security-Policy'):
            response['Content-Security-Policy'] = "default-src 'self'"
        return response
