import secrets
from datetime import timedelta, datetime, timezone

import jwt
from jwt import InvalidTokenError
from fastapi import Response, Request
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import SessionDep
from app.api.request_form import OAuth2EmailRequestForm
from app.core.config import settings
from app.core.security import verify_password
from app.exceptions import USER_UNAUTHORIZED_EXCEPTION, INVALID_TOKEN_EXCEPTION, USER_NOT_FOUND_EXCEPTION, INCORRECT_DATA_EXCEPTION
from app.models import RefreshTokenModel
from app.services import UserService


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
    async def login(
        session: AsyncSession,
        form_data: OAuth2EmailRequestForm,
        response: Response,
    ):
        user = await UserService.get_by_email(session, form_data.username)
        if not user:
            raise INCORRECT_DATA_EXCEPTION
        if not verify_password(form_data.password, user.hashed_password):
            raise INCORRECT_DATA_EXCEPTION

        access_payload = {
            "sub": str(user.id),
            "email": user.email,
            "account_type": "user",
        }

        token = AuthenticatorService.create_jwt_token(access_payload)
        response.set_cookie(
            key="token",
            value=token,
            max_age=int(timedelta(days=7).total_seconds()),
            httponly=False,
            secure=settings.app.IS_PROD,
            samesite="lax",
        )


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
