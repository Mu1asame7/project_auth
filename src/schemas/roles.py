from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RoleRequestAdd(BaseModel):
    title: str


class Role(RoleRequestAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UserRoleAdd(BaseModel):
    user_id: int
    role_id: int


class RoleInDB(BaseModel):
    id: int
    title: str

    model_config = ConfigDict(from_attributes=True)