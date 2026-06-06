from pydantic import BaseModel, ConfigDict, EmailStr


class UserRequestAdd(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    middle_name: str
    password: str


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
