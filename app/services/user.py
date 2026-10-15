from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.exceptions import USER_NOT_FOUND_EXCEPTION, USER_ALREADY_CREATED
from app.models.users import UserModel
from app.schemas import UserCreateSchema, UserUpdateSchema


class UserService:
    @classmethod
    async def get_by_id(cls, session: AsyncSession, account_id: UUID) -> UserModel:
        stmt = select(UserModel).where(UserModel.id == account_id)
        return await session.scalar(stmt)

    @classmethod
    async def get_by_email(cls, session: AsyncSession, email: str) -> UserModel:
        stmt = select(UserModel).where(UserModel.email == email)
        return await session.scalar(stmt)

    @classmethod
    async def create(cls, session: AsyncSession, account_data: UserCreateSchema) -> UserModel:
        if await cls.get_by_email(session, account_data.email):
            raise USER_ALREADY_CREATED

        data = account_data.model_dump(exclude={"password"})
        data["hashed_password"] = get_password_hash(account_data.password)
        new_account = UserModel(**data)

        session.add(new_account)
        await session.commit()
        await session.refresh(new_account)
        return new_account

    @classmethod
    async def update(cls, session: AsyncSession, account_data: UserUpdateSchema, account_id: UUID) -> dict:
        account = await cls.get_by_id(session, account_id)
        if account is None:
            raise USER_NOT_FOUND_EXCEPTION

        update_data = account_data.model_dump(exclude_unset=True)
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(account_data.password)
            del update_data["password"]
        for key, value in update_data.items():
            if value != "":
                setattr(account, key, value)

        session.add(account)
        await session.commit()
        await session.refresh(account)
        return {"ok": True}

    @classmethod
    async def delete(cls, session: AsyncSession, account_id: UUID) -> dict:
        account = await cls.get_by_id(session, account_id)
        if account is None:
            raise USER_NOT_FOUND_EXCEPTION

        await session.delete(account)
        await session.commit()
        return {"ok": True}