from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, status

import jwt
from pwdlib import PasswordHash
import hashlib

from src.config import settings


class AuthService:
    password_hash = PasswordHash.recommended()

    @staticmethod
    def get_token_expire(is_refresh: bool = False) -> datetime:
        if is_refresh:
            return datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        return datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    @staticmethod
    def create_token(data: dict, is_refresh: bool = False) -> str:
        to_encode = data.copy()
        expire = AuthService.get_token_expire(is_refresh)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt

    @staticmethod
    def hash_token(token: str) -> str:
        return hashlib.sha256(token.encode()).hexdigest()

    def hash_password(self, password: str) -> str:
        return self.password_hash.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return self.password_hash.verify(password, hashed_password)

    @staticmethod
    def encode_token(token: str) -> dict:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except jwt.exceptions.DecodeError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Невалидный токен")
