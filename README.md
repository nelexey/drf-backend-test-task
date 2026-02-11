# AIHunt - Система аутентификации и авторизации

Собственная реализация системы аутентификации и авторизации на Django REST Framework.
Система не использует стандартные механизмы Django auth "из коробки" — токены и проверка
прав реализованы вручную.


## Быстрый запуск

Для запуска нужен только Docker:

```bash
docker-compose up --build
```

После запуска будут доступны:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

При первом запуске автоматически происходит:
1. Создание и применение миграций БД
2. Заполнение базы тестовыми данными через команду `python manage.py seed_data`

Команда seed_data создает роли, разрешения, ресурсы и трёх тестовых пользователей.
Это всё прописано в docker-compose.yml в секции command для backend-сервиса.


## Тестовые аккаунты

- admin@test.com / admin123 — администратор, полный доступ
- moderator@test.com / moder123 — модератор, может управлять статьями  
- user@test.com / user1234 — обычный пользователь, только чтение


## Архитектура системы доступа

Система построена на модели RBAC (Role-Based Access Control).

Основные сущности:

**users** — пользователи системы. Хранит email, ФИО, хеш пароля и флаг is_active.
При "удалении" аккаунта пользователь не удаляется физически, а помечается is_active=False.

**auth_tokens** — токены аутентификации. Генерируются при логине, имеют срок действия.
Это собственная реализация, не Session и не JWT.

**roles** — роли: user, moderator, admin.

**resources** — ресурсы системы, к которым применяется контроль доступа.
Сейчас это: articles, users, roles.

**permissions** — разрешения. Связывают ресурс с действием (read, create, update, delete).

**role_permissions** — какие разрешения есть у каждой роли (many-to-many).

**user_roles** — какая роль назначена пользователю.

Связи: User -> UserRole -> Role -> RolePermission -> Permission -> Resource


## Как работает авторизация

1. Клиент отправляет запрос с заголовком `Authorization: Token <токен>`
2. Если токена нет или он невалидный/просроченный — возвращается 401
3. Если токен валидный, определяется пользователь и его роль
4. Проверяется, есть ли у роли разрешение на запрашиваемый ресурс и действие
5. Если разрешения нет — возвращается 403
6. Если всё ок — выполняется запрос


## Права по ролям

user — может только читать статьи (articles:read)

moderator — полный доступ к статьям (read, create, update, delete)

admin — полный доступ ко всему, включая управление пользователями и ролями


## API

Аутентификация:
- POST /api/auth/register/ — регистрация
- POST /api/auth/login/ — вход, возвращает токен
- POST /api/auth/logout/ — выход
- GET /api/auth/profile/ — получить профиль
- PATCH /api/auth/profile/ — обновить профиль
- DELETE /api/auth/profile/ — мягкое удаление аккаунта

Управление доступом (только для admin):
- GET /api/access/roles/ — список ролей с их правами
- GET /api/access/users/ — список пользователей
- POST /api/access/user-roles/ — назначить роль пользователю

Статьи (Mock-данные, таблица в БД не создается):
- GET /api/articles/ — список статей
- POST /api/articles/ — создать статью (moderator+)
- PUT /api/articles/{id}/ — редактировать (moderator+)
- DELETE /api/articles/{id}/ — удалить (moderator+)


## Стек

- Backend: Django 4.2, Django REST Framework
- Database: PostgreSQL 15
- Frontend: Vue 3, Vite, TailwindCSS
- Развертывание: Docker Compose


## Структура проекта

```
backend/
  apps/
    users/          — модель пользователя, токены, аутентификация
    access_control/ — роли, разрешения, ресурсы, RBAC логика
    articles/       — mock viewset для демонстрации работы системы
  config/           — настройки Django

frontend/
  src/
    views/          — страницы Login, Register, Home, Admin
    api/            — axios клиент
```
