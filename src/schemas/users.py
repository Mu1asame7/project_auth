from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRequestAdd(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    middle_name: str
    password: str
    password_confirm: str


class UserAdd(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    middle_name: str
    hashed_password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class User(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserWithHashedPassword(User):
    hashed_password: str


class UserUpdate(BaseModel):
    first_name: str | None = Field(None)
    last_name: str | None = Field(None)
    middle_name: str | None = Field(None)
