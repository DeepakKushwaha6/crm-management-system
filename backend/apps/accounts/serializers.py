from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import Organization, OrganizationMembership, Department, Team, AuditLog

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'full_name', 'phone', 'avatar', 'created_at']
        read_only_fields = ['id', 'created_at']


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, validators=[validate_password])
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    organization_name = serializers.CharField(max_length=255)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('A user with this email already exists.')
        return value

    def create(self, validated_data):
        from django.utils.text import slugify
        import uuid

        org_name = validated_data.pop('organization_name')
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)

        base_slug = slugify(org_name)[:80] or 'org'
        slug = base_slug
        counter = 1
        while Organization.objects.filter(slug=slug).exists():
            slug = f'{base_slug}-{counter}'
            counter += 1

        organization = Organization.objects.create(name=org_name, slug=slug)
        OrganizationMembership.objects.create(
            user=user, organization=organization, role='org_admin'
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = [
            'id', 'name', 'slug', 'plan', 'settings', 'logo', 'website',
            'industry', 'size', 'is_active', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'department', 'created_at']
        read_only_fields = ['id', 'created_at']


class MembershipSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.UUIDField(write_only=True, required=False)
    email = serializers.EmailField(write_only=True, required=False)
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = OrganizationMembership
        fields = [
            'id', 'user', 'user_id', 'email', 'first_name', 'last_name',
            'role', 'department', 'team', 'is_active', 'joined_at',
        ]
        read_only_fields = ['id', 'joined_at']


class AuditLogSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = AuditLog
        fields = [
            'id', 'user_email', 'action', 'resource_type', 'resource_id',
            'details', 'ip_address', 'created_at',
        ]
