from rest_framework import status, generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from django.utils.text import slugify

from core.permissions import CanManageUsers, IsReadOnlyOrAbove
from core.thread_locals import get_current_organization, get_current_membership
from .models import Organization, OrganizationMembership, Department, Team, AuditLog
from .serializers import (
    UserSerializer, RegisterSerializer, LoginSerializer,
    OrganizationSerializer, MembershipSerializer,
    DepartmentSerializer, TeamSerializer, AuditLogSerializer,
)

User = get_user_model()


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        membership = user.memberships.select_related('organization').first()
        return Response({
            'user': UserSerializer(user).data,
            'organization': OrganizationSerializer(membership.organization).data if membership else None,
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            },
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            request,
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
        )
        if not user:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        if not user.is_active:
            return Response({'error': 'Account is disabled'}, status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(user)
        memberships = MembershipSerializer(
            user.memberships.select_related('organization').all(), many=True
        ).data

        AuditLog.objects.create(
            user=user, action='login', resource_type='user',
            resource_id=str(user.id),
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
        )

        return Response({
            'user': UserSerializer(user).data,
            'memberships': memberships,
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            },
        })


class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
        except Exception:
            pass
        return Response({'message': 'Logged out successfully'})


class MeView(APIView):
    def get(self, request):
        membership = get_current_membership()
        data = UserSerializer(request.user).data
        if membership:
            data['current_organization'] = OrganizationSerializer(membership.organization).data
            data['role'] = membership.role
        return Response(data)

    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class OrganizationViewSet(viewsets.ModelViewSet):
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated, IsReadOnlyOrAbove]

    def get_queryset(self):

    # drf-spectacular schema generation
        if getattr(self, "swagger_fake_view", False):
            return Organization.objects.none()

    # unauthenticated requests
        if not self.request.user.is_authenticated:
            return Organization.objects.none()

        org_ids = OrganizationMembership.objects.filter(
        user=self.request.user,
        is_active=True
        ).values_list("organization_id", flat=True)

        return Organization.objects.filter(id__in=org_ids)

    @action(detail=True, methods=['get', 'post'], url_path='members')
    def members(self, request, pk=None):
        organization = self.get_object()
        if request.method == 'GET':
            memberships = OrganizationMembership.objects.filter(
                organization=organization
            ).select_related('user')
            return Response(MembershipSerializer(memberships, many=True).data)

        if not CanManageUsers().has_permission(request, self):
            return Response({'error': 'Permission denied'}, status=403)

        email = request.data.get('email')
        role = request.data.get('role', 'sales_executive')
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'first_name': request.data.get('first_name', ''),
                'last_name': request.data.get('last_name', ''),
            }
        )
        if created:
            user.set_unusable_password()
            user.save()

        membership, mem_created = OrganizationMembership.objects.get_or_create(
            user=user, organization=organization,
            defaults={'role': role}
        )
        if not mem_created:
            membership.role = role
            membership.save()

        return Response(MembershipSerializer(membership).data, status=201)


class DepartmentViewSet(viewsets.ModelViewSet):
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated, CanManageUsers]

    def get_queryset(self):
        org = get_current_organization()
        if not org:
            return Department.objects.none()
        return Department.objects.filter(organization=org)

    def perform_create(self, serializer):
        serializer.save(organization=get_current_organization())


class TeamViewSet(viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated, CanManageUsers]

    def get_queryset(self):
        org = get_current_organization()
        if not org:
            return Team.objects.none()
        return Team.objects.filter(organization=org)

    def perform_create(self, serializer):
        serializer.save(organization=get_current_organization())


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated, CanManageUsers]

    def get_queryset(self):
        org = get_current_organization()
        if not org:
            return AuditLog.objects.none()
        return AuditLog.objects.filter(organization=org)
