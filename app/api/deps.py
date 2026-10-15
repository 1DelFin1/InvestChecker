from uuid import UUID

from jwt import InvalidTokenError
from typing import Annotated, AsyncGenerator

from fastapi import Depends, status, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import USER_UNAUTHORIZED_EXCEPTION, USER_NOT_FOUND_EXCEPTION, INVALID_TOKEN_EXCEPTION
from app.core.database import async_session_factory
from app.services.user import UserService
from app.services.auth import AuthenticatorService
from app.schemas import UserInDBSchema


async def get_session() -> AsyncGenerator:
    async with async_session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


SessionDep = Annotated[AsyncSession, Depends(get_session)]

async def get_current_active_auth_user(request: Request, session: SessionDep):
    token = request.cookies.get("token")
    if not token:
        raise USER_UNAUTHORIZED_EXCEPTION

    try:
        payload = AuthenticatorService.decode_jwt_token(token)
    except InvalidTokenError:
        raise INVALID_TOKEN_EXCEPTION

    user = await UserService.get_by_email(session, payload.get("email"))
    if not user:
        raise USER_NOT_FOUND_EXCEPTION
    return user

async def ensure_user_access(
    user_id: UUID,
    current_user: UserInDBSchema = Depends(get_current_active_auth_user),
) -> UserInDBSchema:
    if not current_user.is_superuser and current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return current_user