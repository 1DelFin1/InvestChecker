from uuid import UUID

from fastapi import APIRouter, Depends

from app.api.deps import SessionDep, ensure_user_access, get_current_active_auth_user
from app.schemas import UserUpdateSchema, UserInDBSchema, UserCreateSchema
from app.services import UserService

users_router = APIRouter(prefix="/api/v1/users", tags=["users"])


@users_router.get("/me")
async def get_current_user(
    user_data: UserInDBSchema = Depends(get_current_active_auth_user),
):
    return user_data


@users_router.post("")
async def create_user(session: SessionDep, user_data: UserCreateSchema):
    user = await UserService.create(session, user_data)
    return user


@users_router.get("/{user_id}")
async def get_user_by_id(session: SessionDep, user_id: UUID, _ = Depends(ensure_user_access)):
    user = await UserService.get_by_id(session, user_id)
    return user


@users_router.patch("/{user_id}")
async def update_user(
    session: SessionDep, user_data: UserUpdateSchema, user_id: UUID, _ = Depends(ensure_user_access)
):
    user = await UserService.update(session, user_data, user_id)
    return user


@users_router.delete("/{user_id}")
async def delete_user(session: SessionDep, user_id: UUID, _ = Depends(ensure_user_access)):
    user = await UserService.delete(session, user_id)
    return user
