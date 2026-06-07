from sqlalchemy import select

from src.models.roles import RolesORM, UserRoles
from src.repo.mappers.mappers import RolesDataMapper, RoleMapper, UserRolesMapper
from src.repo.base import BaseRepo
from src.schemas.roles import RoleInDB


class RolesRepository(BaseRepo):
    model = RolesORM
    mapper = RolesDataMapper


class UserRolesRepository(BaseRepo):
    model = UserRoles
    mapper = UserRolesMapper
    role_mapper = RoleMapper

    async def get_roles_by_user_id(self, user_id: int) -> list[RoleInDB]:
        stmt = (
            select(RolesORM)
            .join(UserRoles, UserRoles.role_id == RolesORM.id)
            .where(UserRoles.user_id == user_id)
        )
        result = await self.session.execute(stmt)
        orm_roles = result.scalars().all()

        return [self.role_mapper.map_to_domain_entity(role) for role in orm_roles]
