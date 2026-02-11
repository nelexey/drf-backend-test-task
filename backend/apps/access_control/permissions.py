from rest_framework.permissions import BasePermission
from .models import UserRole, RolePermission


class HasResourcePermission(BasePermission):
    def __init__(self, resource_name, action):
        self.resource_name = resource_name
        self.action = action

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        user_roles = UserRole.objects.filter(user=request.user).values_list('role_id', flat=True)
        
        has_perm = RolePermission.objects.filter(
            role_id__in=user_roles,
            permission__resource__name=self.resource_name,
            permission__action=self.action
        ).exists()
        
        return has_perm


def check_permission(user, resource_name, action):
    if not user or not user.is_authenticated:
        return False
    
    user_roles = UserRole.objects.filter(user=user).values_list('role_id', flat=True)
    
    return RolePermission.objects.filter(
        role_id__in=user_roles,
        permission__resource__name=resource_name,
        permission__action=action
    ).exists()


def get_user_role(user):
    user_role = UserRole.objects.filter(user=user).select_related('role').first()
    return user_role.role.name if user_role else None


def is_admin(user):
    return get_user_role(user) == 'admin'


def is_moderator(user):
    role = get_user_role(user)
    return role in ['admin', 'moderator']
