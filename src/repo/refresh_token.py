from src.models.refresh_token import RefreshToken
from src.repo.base import BaseRepo
from src.repo.mappers.mappers import RefreshTokenDataMapper


class RefreshTokenRepository(BaseRepo):
    model = RefreshToken
    mapper = RefreshTokenDataMapper
