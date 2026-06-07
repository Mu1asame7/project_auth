from src.models.roles import RolesORM, UserRoles
from src.repo.mappers.mappers import RolesDataMapper
from src.repo.base import BaseRepo


class RolesRepository(BaseRepo):
    model = RolesORM
    mapper = RolesDataMapper


class UserRolesRepository(BaseRepo):
    model = UserRoles
