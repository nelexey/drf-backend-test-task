from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RoleViewSet, PermissionViewSet, ResourceViewSet,
    UserRoleView, RolePermissionView, UsersListView
)

router = DefaultRouter()
router.register('roles', RoleViewSet)
router.register('permissions', PermissionViewSet)
router.register('resources', ResourceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('user-roles/', UserRoleView.as_view(), name='user-roles'),
    path('role-permissions/', RolePermissionView.as_view(), name='role-permissions'),
    path('users/', UsersListView.as_view(), name='users-list'),
]
