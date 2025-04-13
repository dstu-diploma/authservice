from fastapi import HTTPException
from .dto import AccessJWTPayloadDto, RefreshJWTPayloadDto, UserJWTDto
from jose import ExpiredSignatureError, JWTError, jwt
from app.models.user_tokens import UserTokensModel
from datetime import datetime, timedelta
from os import environ

JWT_SECRET = environ.get("JWT_SECRET", "zaza")


async def get_user_by_id(user_id: int):
    user = await UserTokensModel.get_or_none(user_id=user_id)

    if user is None:
        raise HTTPException(
            status_code=404, detail="User with providen UserID does not exists!"
        )

    return user


async def generate_refresh_token(user_id: int, role: str):
    user = await get_user_by_id(user_id)
    await user.increase_revision()

    payload = RefreshJWTPayloadDto(
        user_id=user_id,
        role=role,
        token_revision=user.token_revision,
        exp=datetime.now() + timedelta(days=7),
    )

    await user.save()
    return jwt.encode(
        payload.model_dump(),
        JWT_SECRET,
    )


async def validate_refresh_token(token: str):
    try:
        raw_payload = jwt.decode(token, JWT_SECRET)
        payload = RefreshJWTPayloadDto(**raw_payload)
        user = await get_user_by_id(payload.user_id)

        return user.verify_revision(payload.token_revision), payload
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=403, detail="Refresh token has expired!"
        )
    except JWTError:
        raise HTTPException(
            status_code=403, detail="An error occured during JWT parsing!"
        )


async def generate_access_token(user_id: int, refresh_token: str):
    is_valid, refresh_payload = await validate_refresh_token(refresh_token)
    if not is_valid:
        raise HTTPException(
            status_code=401,
            detail="Refresh token is invalid! Please generate a new one",
        )
    elif refresh_payload.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="This token is owned by another user!",
        )

    payload = AccessJWTPayloadDto(
        user_id=refresh_payload.user_id,
        role=refresh_payload.role,
        exp=datetime.now() + timedelta(minutes=10),
    )

    return jwt.encode(
        payload.model_dump(),
        JWT_SECRET,
    )


async def generate_key_pair(user_id: int, role: str):
    refresh = await generate_refresh_token(user_id, role)
    access = await generate_access_token(user_id, refresh)

    return access, refresh


async def init_user(user_id: int, role: str):
    await UserTokensModel.create(user_id=user_id)
    access, refresh = await generate_key_pair(user_id, role)
    return UserJWTDto(access_token=access, refresh_token=refresh)
