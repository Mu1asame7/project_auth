from pydantic import EmailStr
from sqlalchemy import select, update

from src.repo.mappers.mappers import UserDataMapper
from src.schemas.users import UserWithHashedPassword
from src.models.users import UsersORM
from src.repo.base import BaseRepo


class UsersRepository(BaseRepo):
    model = UsersORM
    mapper = UserDataMapper

    async def get_user_with_hashed_password_active(self, email: EmailStr):
        query = select(self.model).filter_by(email=email, is_active=True)
        result = await self.session.execute(query)
        model = result.scalars().one()
        return UserWithHashedPassword.model_validate(model)

    async def delete(self, user_id: int):
        delete_data_stmt = update(self.model).filter_by(id=user_id).values(is_active=False)
        await self.session.execute(delete_data_stmt)