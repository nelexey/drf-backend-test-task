from django.core.management.base import BaseCommand
from apps.users.models import User
from apps.access_control.models import Role, Permission, Resource, UserRole, RolePermission


class Command(BaseCommand):
    help = 'Заполнение БД тестовыми данными'

    def handle(self, *args, **options):
        self.stdout.write('Создание ресурсов...')
        articles_resource, _ = Resource.objects.get_or_create(
            name='articles',
            defaults={'description': 'Управление статьями'}
        )
        users_resource, _ = Resource.objects.get_or_create(
            name='users',
            defaults={'description': 'Управление пользователями'}
        )
        roles_resource, _ = Resource.objects.get_or_create(
            name='roles',
            defaults={'description': 'Управление ролями'}
        )

        self.stdout.write('Создание разрешений...')
        permissions = {}
        for resource in [articles_resource, users_resource, roles_resource]:
            for action in ['read', 'create', 'update', 'delete']:
                perm, _ = Permission.objects.get_or_create(
                    resource=resource,
                    action=action
                )
                permissions[f'{resource.name}_{action}'] = perm

        self.stdout.write('Создание ролей...')
        user_role, _ = Role.objects.get_or_create(
            name='user',
            defaults={'description': 'Обычный пользователь'}
        )
        moderator_role, _ = Role.objects.get_or_create(
            name='moderator',
            defaults={'description': 'Модератор контента'}
        )
        admin_role, _ = Role.objects.get_or_create(
            name='admin',
            defaults={'description': 'Администратор системы'}
        )

        self.stdout.write('Назначение разрешений ролям...')
        RolePermission.objects.filter(role=user_role).delete()
        RolePermission.objects.create(role=user_role, permission=permissions['articles_read'])

        RolePermission.objects.filter(role=moderator_role).delete()
        for action in ['read', 'create', 'update', 'delete']:
            RolePermission.objects.create(role=moderator_role, permission=permissions[f'articles_{action}'])

        RolePermission.objects.filter(role=admin_role).delete()
        for perm in permissions.values():
            RolePermission.objects.create(role=admin_role, permission=perm)

        self.stdout.write('Создание тестовых пользователей...')
        admin_user, created = User.objects.get_or_create(
            email='admin@test.com',
            defaults={
                'first_name': 'Админ',
                'last_name': 'Системный',
                'patronymic': 'Главный'
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
        UserRole.objects.get_or_create(user=admin_user, role=admin_role)

        moderator_user, created = User.objects.get_or_create(
            email='moderator@test.com',
            defaults={
                'first_name': 'Модератор',
                'last_name': 'Контента',
                'patronymic': ''
            }
        )
        if created:
            moderator_user.set_password('moder123')
            moderator_user.save()
        UserRole.objects.get_or_create(user=moderator_user, role=moderator_role)

        regular_user, created = User.objects.get_or_create(
            email='user@test.com',
            defaults={
                'first_name': 'Пользователь',
                'last_name': 'Обычный',
                'patronymic': ''
            }
        )
        if created:
            regular_user.set_password('user1234')
            regular_user.save()
        UserRole.objects.get_or_create(user=regular_user, role=user_role)

        self.stdout.write(self.style.SUCCESS('Seed данные успешно созданы!'))
        self.stdout.write('Тестовые аккаунты:')
        self.stdout.write('  admin@test.com / admin123 (администратор)')
        self.stdout.write('  moderator@test.com / moder123 (модератор)')
        self.stdout.write('  user@test.com / user1234 (пользователь)')
