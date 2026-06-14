from rest_framework import permissions
from core.thread_locals import get_current_membership


class RolePermission(permissions.BasePermission):
    allowed_roles = []

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        membership = get_current_membership()
        if not membership:
            return False
        if not self.allowed_roles:
            return True
        return membership.role in self.allowed_roles


class IsSuperAdmin(RolePermission):
    allowed_roles = ['super_admin']


class IsOrgAdmin(RolePermission):
    allowed_roles = ['super_admin', 'org_admin']


class IsSalesManager(RolePermission):
    allowed_roles = ['super_admin', 'org_admin', 'sales_manager']


class IsSalesExecutive(RolePermission):
    allowed_roles = ['super_admin', 'org_admin', 'sales_manager', 'sales_executive']


class IsReadOnlyOrAbove(RolePermission):
    allowed_roles = ['super_admin', 'org_admin', 'sales_manager', 'sales_executive', 'read_only']

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            membership = get_current_membership()
            if request.user.is_superuser:
                return True
            return membership is not None
        return super().has_permission(request, view)


class CanWriteCRM(IsSalesExecutive):
    pass


class CanManageUsers(IsOrgAdmin):
    pass
