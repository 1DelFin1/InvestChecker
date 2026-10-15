from fastapi import APIRouter

from app.api.routers.auth import auth_router
from app.api.routers.users import users_router

main_router = APIRouter()
main_router.include_router(users_router)
main_router.include_router(auth_router)

__all__ = [
    "main_router",
]
