from rest_framework_simplejwt.authentication import JWTAuthentication
from apps.accounts.models import Organization, OrganizationMembership
from .thread_locals import set_current_organization, set_current_membership


class TenantJWTAuthentication(JWTAuthentication):
    """JWT authentication that also resolves tenant context from headers."""

    def authenticate(self, request):
        result = super().authenticate(request)
        if result is None:
            return None

        user, validated_token = result
        self._set_tenant_context(request, user)
        return user, validated_token

    def _set_tenant_context(self, request, user):
        org_id = (
            request.headers.get('X-Organization-ID')
            or request.META.get('HTTP_X_ORGANIZATION_ID')
        )

        if org_id:
            try:
                organization = Organization.objects.get(id=org_id)
                membership = OrganizationMembership.objects.get(
                    user=user, organization=organization, is_active=True,
                )
                set_current_organization(organization)
                set_current_membership(membership)
                request.organization = organization
                request.membership = membership
                return
            except (Organization.DoesNotExist, OrganizationMembership.DoesNotExist):
                pass

        membership = OrganizationMembership.objects.filter(
            user=user, is_active=True,
        ).select_related('organization').first()

        if membership:
            set_current_organization(membership.organization)
            set_current_membership(membership)
            request.organization = membership.organization
            request.membership = membership
