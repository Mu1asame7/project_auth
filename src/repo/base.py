from pydantic import BaseModel
from sqlalchemy import insert

from src.schemas.users import UserWithHashedPassword


class BaseRepo:
    model = None
    mapper = None

    def __init__(self, session):
        self.session = session

    async def add(self, data: BaseModel):
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_data_stmt)
        model = result.scalars().one()
        return UserWithHashedPassword.model_validate(model)