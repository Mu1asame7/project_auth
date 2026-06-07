from typing import Annotated

from fastapi import Depends, HTTPException, Request, status

from src.database import async_session_maker
from src.service.auth import AuthService
from src.utils.db_manager import DBManager


def get_access_token(request: Request) -> str:
    token = request.cookies.get("access_token", None)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return token


def get_current_user_id(token: str = Depends(get_access_token)) -> int:
    data = AuthService().encode_token(token)
    return data["user_id"]


UserIdDep = Annotated[int, Depends(get_current_user_id)]


def get_db_manager():
    return DBManager(session_factory=async_session_maker)


async def get_db():
    async with get_db_manager() as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]


def get_refresh_token(request: Request) -> str:
    token = request.cookies.get("refresh_token", None)
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token not found")
    return token


def get_hashed_refresh_token(token: str = Depends(get_refresh_token)) -> str:
    if not token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    return AuthService().hash_token(token)


RefreshTokenDep = Annotated[str, Depends(get_hashed_refresh_token)]
