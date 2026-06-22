from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.user import UserRole


class Token(BaseModel):
    """OAuth2 token response."""

    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """JWT token payload."""

    sub: str | None = None
    exp: int | None = None


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)
    role: UserRole
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)
