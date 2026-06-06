from src.models.users import UsersORM
from src.repo.mappers.base import DataMapper
from src.schemas.users import User


class UserDataMapper(DataMapper):
    db_model = UsersORM
    schema = User
