from pydantic import EmailStr
from sqlalchemy import select

from src.repo.mappers.mappers import UserDataMapper
from src.schemas.users import UserWithHashedPassword
from src.models.users import UsersORM
from src.repo.base import BaseRepo


class UsersRepository(BaseRepo):
    model = UsersORM
    mapper = UserDataMapper

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one()
        return UserWithHashedPassword.model_validate(model)