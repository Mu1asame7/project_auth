from pydantic import BaseModel
from sqlalchemy import insert, update, delete


class BaseRepo:
    model = None
    mapper = None

    def __init__(self, session):
        self.session = session

    async def add(self, data: BaseModel):
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_data_stmt)
        model = result.scalars().one()
        return self.mapper.map_to_domain_entity(model)

    async def edit(self, data: BaseModel, is_patch: bool = False, **filter_by) -> None:
        update_data_stmt = update(self.model).filter_by(**filter_by).values(**data.model_dump(exclude_unset=is_patch))
        await self.session.execute(update_data_stmt)

    async def delete(self, **filter_by):
        delete_data_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_data_stmt)