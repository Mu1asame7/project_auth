from src.models.refresh_token import RefreshToken
from src.models.roles import RolesORM, UserRoles
from src.models.users import UsersORM
from src.repo.mappers.base import DataMapper
from src.schemas.refresh_token import RefreshTokenDB
from src.schemas.roles import Role, RoleInDB, UserRoleInDB
from src.schemas.users import User


class UserDataMapper(DataMapper):
    db_model = UsersORM
    schema = User


class RefreshTokenDataMapper(DataMapper):
    db_model = RefreshToken
    schema = RefreshTokenDB


class RolesDataMapper(DataMapper):
    db_model = RolesORM
    schema = Role


class RoleMapper(DataMapper):
    model = RolesORM
    schema = RoleInDB


class UserRolesMapper(DataMapper):
    db_model = UserRoles
    schema = UserRoleInDB
