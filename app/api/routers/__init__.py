from fastapi import APIRouter

from app.api.routers.auth import auth_router
from app.api.routers.users import users_router
from app.api.routers.PODs import pods_router

main_router = APIRouter()
main_router.include_router(users_router)
main_router.include_router(auth_router)
main_router.include_router(pods_router)

__all__ = [
    "main_router",
]
