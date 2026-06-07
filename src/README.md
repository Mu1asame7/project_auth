# Система аутентификации и разграничения прав доступа (RBAC)

## Модель данных

- **users** — учётные записи (id, email, hashed_password, first_name, last_name, middle_name, is_active)
- **roles** — роли (id, title)
- **user_roles** — связь пользователей и ролей (user_id, role_id)

Поддерживаемые роли: `admin`, `manager`, `user`.

## Механизм проверки прав

Доступ к эндпоинтам ограничивается декоратором `@RolesChecker(["role"])`, который:

- извлекает `user_id` из JWT-токена
- загружает роли пользователя из базы данных
- сравнивает их с разрешёнными ролями
- при отсутствии нужной роли возвращает ошибку **403 Forbidden**
- при отсутствии аутентификации — **401 Unauthorized**

## API для управления правами (доступен только admin)

- `GET /admin/roles` — список ролей
- `POST /admin/roles` — создание роли
- `PATCH /admin/roles/{role_id}` — редактирование роли
- `DELETE /admin/roles/{role_id}` — удаление роли
- `GET /admin/users/{user_id}/roles` — роли пользователя
- `POST /admin/users/{user_id}/roles` — назначить роль пользователю
- `DELETE /admin/users/{user_id}/roles/{role_id}` — отозвать роль