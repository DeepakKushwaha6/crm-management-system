from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Organization, OrganizationMembership, Department, Team, AuditLog


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_active', 'is_staff']
    list_filter = ['is_active', 'is_staff']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['email']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal', {'fields': ('first_name', 'last_name', 'phone', 'avatar')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2')}),
    )


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'plan', 'is_active', 'created_at']
    search_fields = ['name', 'slug']


@admin.register(OrganizationMembership)
class OrganizationMembershipAdmin(admin.ModelAdmin):
    list_display = ['user', 'organization', 'role', 'is_active']
    list_filter = ['role', 'is_active']


admin.site.register(Department)
admin.site.register(Team)
admin.site.register(AuditLog)
