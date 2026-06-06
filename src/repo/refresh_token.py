from src.repo.mappers.mappers import RefreshTokenDataMapper
from src.models.refresh_token import RefreshToken
from src.repo.base import BaseRepo


class RefreshTokenRepository(BaseRepo):
    model = RefreshToken
    mapper = RefreshTokenDataMapper