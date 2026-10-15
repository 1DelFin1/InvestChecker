from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserBaseSchema(BaseModel):
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    email: EmailStr = Field(max_length=255)
    is_active: bool = True
    is_superuser: bool = False


class UserCreateSchema(UserBaseSchema):
    password: str = Field(max_length=40)


class UserUpdateSchema(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    password: str | None = None


class UserInDBSchema(UserBaseSchema):
    id: UUID
    hashed_password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int
    user_id: UUID

class LoginRequest(BaseModel):
    email: EmailStr
    password: str