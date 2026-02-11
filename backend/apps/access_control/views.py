from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Role, Permission, Resource, UserRole, RolePermission
from .serializers import (
    RoleSerializer, PermissionSerializer, ResourceSerializer,
    UserRoleSerializer, AssignRoleSerializer, RolePermissionUpdateSerializer
)
from .permissions import is_admin
from apps.users.models import User
from apps.users.serializers import UserSerializer


class AdminRequiredMixin:
    def check_admin(self, request):
        if not is_admin(request.user):
            return Response(
                {'error': 'Доступ запрещен. Требуются права администратора'},
                status=status.HTTP_403_FORBIDDEN
            )
        return None


class RoleViewSet(viewsets.ModelViewSet, AdminRequiredMixin):
    queryset = Role.objects.prefetch_related('permissions')
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        admin_check = self.check_admin(request)
        if admin_check:
            return admin_check
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        admin_check = self.check_admin(request)
        if admin_check:
            return admin_check
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        admin_check = self.check_admin(request)
        if admin_check:
            return admin_check
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        admin_check = self.check_admin(request)
        if admin_check:
            return admin_check
        return super().destroy(request, *args, **kwargs)


class PermissionViewSet(viewsets.ReadOnlyModelViewSet, AdminRequiredMixin):
    queryset = Permission.objects.select_related('resource')
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        admin_check = self.check_admin(request)
        if admin_check:
            return admin_check
        return super().list(request, *args, **kwargs)


class ResourceViewSet(viewsets.ModelViewSet, AdminRequiredMixin):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        admin_check = self.check_admin(request)
        if admin_check:
            return admin_check
        return super().list(request, *args, **kwargs)


class UserRoleView(APIView, AdminRequiredMixin):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        admin_check = self.check_admin(request)
        if admin_check:
            return admin_check
        user_roles = UserRole.objects.select_related('user', 'role').all()
        return Response(UserRoleSerializer(user_roles, many=True).data)

    def post(self, request):
        admin_check = self.check_admin(request)
        if admin_check:
            return admin_check
        
        serializer = AssignRoleSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(id=serializer.validated_data['user_id'])
            role = Role.objects.get(name=serializer.validated_data['role_name'])
            
            UserRole.objects.filter(user=user).delete()
            user_role = UserRole.objects.create(user=user, role=role)
            
            return Response(UserRoleSerializer(user_role).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RolePermissionView(APIView, AdminRequiredMixin):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        admin_check = self.check_admin(request)
        if admin_check:
            return admin_check
        
        serializer = RolePermissionUpdateSerializer(data=request.data)
        if serializer.is_valid():
            role_id = serializer.validated_data['role_id']
            permission_ids = serializer.validated_data['permission_ids']
            
            try:
                role = Role.objects.get(id=role_id)
            except Role.DoesNotExist:
                return Response({'error': 'Роль не найдена'}, status=status.HTTP_404_NOT_FOUND)
            
            RolePermission.objects.filter(role=role).delete()
            
            for perm_id in permission_ids:
                try:
                    permission = Permission.objects.get(id=perm_id)
                    RolePermission.objects.create(role=role, permission=permission)
                except Permission.DoesNotExist:
                    pass
            
            return Response(RoleSerializer(role).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersListView(APIView, AdminRequiredMixin):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        admin_check = self.check_admin(request)
        if admin_check:
            return admin_check
        users = User.objects.filter(is_active=True).prefetch_related('user_roles__role')
        return Response(UserSerializer(users, many=True).data)
