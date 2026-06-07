from datetime import UTC, datetime

from fastapi import APIRouter, HTTPException, Response

from src.api.dependencies import DBDep, RefreshTokenDep, UserIdDep
from src.schemas.refresh_token import RefreshTokenAdd, RefreshTokenUpdate
from src.schemas.roles import UserRoleAdd
from src.schemas.users import UserAdd, UserLogin, UserRequestAdd, UserUpdate
from src.service.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(
    db: DBDep,
    data: UserRequestAdd,
):
    if data.password != data.password_confirm:
        raise HTTPException(status_code=401, detail="Некорректный пароль")
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(
        email=data.email,
        first_name=data.first_name,
        last_name=data.last_name,
        middle_name=data.middle_name,
        hashed_password=hashed_password,
    )
    user = await db.users.add(new_user_data)

    standard_roles_ids = [2]
    room_facilities_data = [UserRoleAdd(user_id=user.id, role_id=r_id) for r_id in standard_roles_ids]
    await db.user_roles.add_bulk(room_facilities_data)
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
    new_refresh_token = RefreshTokenAdd(
        token_hash=AuthService().hash_token(refresh_token),
        user_id=user.id,
        expires_at=AuthService().get_token_expire(is_refresh=True),
    )
    await db.refresh_token.add(new_refresh_token)
    await db.commit()
    response.set_cookie("access_token", access_token, httponly=True)
    response.set_cookie("refresh_token", refresh_token, httponly=True)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/refresh")
async def refresh_access_token(
    db: DBDep,
    response: Response,
    hashed_refresh_token: RefreshTokenDep,
):
    token_entry = await db.refresh_token.get_one_or_none(token_hash=hashed_refresh_token)

    AuthService.validate_refresh_token_entry(token_entry)

    await db.refresh_token.edit(
        RefreshTokenUpdate(revoked_at=datetime.now(UTC)),
        is_patch=True,
        token_hash=hashed_refresh_token,
    )

    user_id = token_entry.user_id

    access_token = AuthService().create_token({"user_id": user_id})
    refresh_token = AuthService().create_token({"user_id": user_id}, is_refresh=True)

    new_hashed_refresh_token = AuthService().hash_token(refresh_token)
    await db.refresh_token.add(
        RefreshTokenAdd(
            token_hash=new_hashed_refresh_token,
            user_id=user_id,
            expires_at=AuthService().get_token_expire(is_refresh=True),
        )
    )
    await db.commit()

    response.set_cookie("access_token", access_token, httponly=True)
    response.set_cookie("refresh_token", refresh_token, httponly=True)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.patch("/me")
async def update_user(db: DBDep, user_data: UserUpdate, user_id: UserIdDep):
    await db.users.edit(user_data, is_patch=True, id=user_id)
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
    db: DBDep,
    response: Response,
    hashed_refresh_token: RefreshTokenDep,
):
    await db.refresh_token.edit(
        RefreshTokenUpdate(revoked_at=datetime.now(UTC)),
        is_patch=True,
        token_hash=hashed_refresh_token,
    )
    await db.commit()
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"status": "OK"}
