from fastapi import APIRouter, Response, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.refresh_token import RefreshTokenAdd
from src.schemas.users import UserRequestAdd, UserAdd, UserLogin, UserUpdate
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
    user = await db.users.get_user_with_hashed_password_active(email=data.email)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    access_token = AuthService().create_token({"user_id": user.id})
    refresh_token = AuthService().create_token({"user_id": user.id}, is_refresh=True)
    print(refresh_token)
    new_refresh_token = RefreshTokenAdd(
        token_hash=AuthService().hash_password(refresh_token),
        user_id=user.id,
        expires_at=AuthService().get_token_expire(is_refresh=True),
    )
    await db.refresh_token.add(new_refresh_token)
    await db.commit()
    response.set_cookie("access_token", access_token)
    response.set_cookie("refresh_token", refresh_token)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.patch("/me")
async def update_user(
        db: DBDep,
        user_data: UserUpdate,
        user_id: UserIdDep
):
    await db.users.edit(
        user_data,
        is_patch=True,
        id=user_id
    )
    await db.commit()

    return {"status": "OK"}


@router.delete("/delete")
async def delete_user(
        db: DBDep,
        user_id: UserIdDep,
        response: Response,
):
    print(user_id)
    await db.users.delete(user_id)
    await db.commit()
    response.delete_cookie("access_token")
    return {"status": "OK"}


@router.post("/logout")
async def logout_user(
        response: Response,
):
    response.delete_cookie("access_token")
    return {"status": "OK"}
