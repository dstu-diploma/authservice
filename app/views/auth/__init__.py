from fastapi import APIRouter, Query, Request
from app.controllers import auth as auth_controller
from .dto import UserWithRoleDto

router = APIRouter(prefix="")


@router.post("/init", response_model=auth_controller.UserJWTDto)
async def init_user(user_dto: UserWithRoleDto):
    return await auth_controller.init_user(user_dto.user_id, user_dto.role)


@router.post("/generate_refresh")
async def generate_refresh_token(user_dto: UserWithRoleDto):
    return await auth_controller.generate_refresh_token(
        user_dto.user_id, user_dto.role
    )


@router.get("/token")
async def generate_access_token(refresh_token: str, user_id: int = Query(ge=0)):
    return await auth_controller.generate_access_token(user_id, refresh_token)
