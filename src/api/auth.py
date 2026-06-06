from fastapi import APIRouter, Response, HTTPException

from src.api.dependencies import DBDep
from src.schemas.users import UserRequestAdd, UserAdd, UserLogin
from src.service.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(
        db: DBDep,
        data: UserRequestAdd,
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(
        email=data.email,
        first_name=data.first_name,
        last_name=data.last_name,
        middle_name=data.middle_name,
        hashed_password=hashed_password
    )
    await db.users.add(new_user_data)
    await db.commit()

    return {"status": "OK"}


@router.post("/login")
async def login_user(
        db: DBDep,
        data: UserLogin,
        response: Response,
):
    user = await db.users.get_user_with_hashed_password(email=data.email)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token, "token_type": "bearer"}



