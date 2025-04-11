from fastapi import APIRouter
from .auth import router as auth_router

main_router = APIRouter(tags=["AuthService"])
main_router.include_router(auth_router)
