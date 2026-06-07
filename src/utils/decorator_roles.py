from fastapi import HTTPException, status
from functools import wraps

from src.api.dependencies import DBDep
from src.repo.roles import UserRolesRepository


class RolesChecker:
    def __init__(self, required_roles: list[str]):
        self.required_roles = required_roles

    def __call__(self, func):
        @wraps(func)
        async def wrapper(
                db: DBDep,
                user_id: int,
                *args, **kwargs
        ):
            user_roles = await UserRolesRepository(db.session).get_roles_by_user_id(user_id)
            role_titles = [role.title for role in user_roles]

            if not any(role in role_titles for role in self.required_roles):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Недостаточно прав!"
                )

            return await func(db=db, user_id=user_id, *args, **kwargs)

        return wrapper