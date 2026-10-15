from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserBaseSchema(BaseModel):
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    email: EmailStr = Field(max_length=255)
    is_active: bool = True
    is_superuser: bool = False


class UserUpdateSchema(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    password: str | None = None


class UserInDBSchema(UserBaseSchema):
    id: UUID
    hashed_password: str


class MagicLinkRequestSchema(BaseModel):
    email: EmailStr
