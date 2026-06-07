from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RoleRequestAdd(BaseModel):
    title: str


class Role(RoleRequestAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoleUpdate(BaseModel):
    title: str | None = None


class UserRoleAdd(BaseModel):
    user_id: int
    role_id: int


class UserRoleAddAdmin(BaseModel):
    role_id: int


class RoleInDB(BaseModel):
    id: int
    title: str

    model_config = ConfigDict(from_attributes=True)


class UserRoleInDB(BaseModel):
    id: int
    user_id: int
    role_id: int

    model_config = ConfigDict(from_attributes=True)