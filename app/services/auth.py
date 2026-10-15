from datetime import timedelta, datetime, timezone

import jwt
from fastapi import Response, BackgroundTasks, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.exceptions import INCORRECT_DATA_EXCEPTION
from app.services import UserService
from app.services.task import TasksService
from app.schemas import MagicLinkRequestSchema


class AuthenticatorService:
    @staticmethod
    def create_jwt_token(
        payload: dict,
        key=settings.jwt.JWT_SECRET_KEY,
        algorithm=settings.jwt.JWT_ALGORITHM,
        expire_minutes=settings.jwt.ACCESS_TOKEN_EXPIRE_MINUTES,
        expire_timedelta: timedelta | None = None,
    ):
        to_encode = payload.copy()
        now = datetime.now(timezone.utc)
        if expire_timedelta:
            expire = now + expire_timedelta
        else:
            expire = now + timedelta(minutes=expire_minutes)

        to_encode.update(
            exp=expire,
            iat=now,
        )
        encoded = jwt.encode(to_encode, key, algorithm)
        return encoded

    @staticmethod
    def decode_jwt_token(
        payload,
        key=settings.jwt.JWT_SECRET_KEY,
        algorithm=settings.jwt.JWT_ALGORITHM,
    ):
        return jwt.decode(payload, key, algorithm)


class AuthorizationService:
    @staticmethod
    async def request(
        session: AsyncSession,
        user_data: MagicLinkRequestSchema,
        background_tasks: BackgroundTasks,
    ):
        user = await UserService.get_by_email(session, user_data.email)
        if not user:
            user = await UserService.create(session, user_data.email)

        access_payload = {
            "sub": str(user.id),
            "email": user.email,
            "is_superuser": user.is_superuser,
            "type": "magic_link",
            "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.jwt.ACCESS_TOKEN_EXPIRE_MINUTES),
        }

        token = AuthenticatorService.create_jwt_token(access_payload)
        link = f"{settings.app.FRONTEND_URL}/auth/verify?token={token}"
        background_tasks.add_task(TasksService.send_magic_link_email, user_data.email, link)


    @classmethod
    async def verify(cls, token: str, response: Response):
        try:
            payload = AuthenticatorService.decode_jwt_token(token)
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")

        if payload["type"] != "magic_link":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token type")

        response.set_cookie(
            key="access_token",
            value=token,
            max_age=int(timedelta(days=7).total_seconds()),
            httponly=False,
            secure=settings.app.IS_PROD,
            samesite="lax",
        )
