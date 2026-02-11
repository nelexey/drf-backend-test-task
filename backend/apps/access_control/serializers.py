from rest_framework import serializers
from .models import Role, Permission, Resource, UserRole, RolePermission
from apps.users.models import User


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['id', 'name', 'description']


class PermissionSerializer(serializers.ModelSerializer):
    resource_name = serializers.CharField(source='resource.name', read_only=True)

    class Meta:
        model = Permission
        fields = ['id', 'resource', 'resource_name', 'action']


class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'permissions']


class UserRoleSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    role_name = serializers.CharField(source='role.name', read_only=True)

    class Meta:
        model = UserRole
        fields = ['id', 'user', 'user_email', 'role', 'role_name']


class AssignRoleSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    role_name = serializers.CharField()

    def validate_user_id(self, value):
        if not User.objects.filter(id=value, is_active=True).exists():
            raise serializers.ValidationError('Пользователь не найден')
        return value

    def validate_role_name(self, value):
        if not Role.objects.filter(name=value).exists():
            raise serializers.ValidationError('Роль не найдена')
        return value


class RolePermissionUpdateSerializer(serializers.Serializer):
    role_id = serializers.IntegerField()
    permission_ids = serializers.ListField(child=serializers.IntegerField())
