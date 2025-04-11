from pydantic import BaseModel
from datetime import datetime


class JWTPayloadDto(BaseModel):
    user_id: int
    token_revision: int
    role: str
    exp: datetime


class UserJWTDto(BaseModel):
    access_token: str
    refresh_token: str
