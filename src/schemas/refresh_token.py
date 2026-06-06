from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class RefreshTokenAdd(BaseModel):
    token_hash: str
    user_id: int
    expires_at: datetime
    revoked_at: datetime | None = Field(None)


class RefreshTokenUpdate(BaseModel):
    revoked_at: datetime | None = Field(None)


class RefreshTokenDB(RefreshTokenAdd):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
