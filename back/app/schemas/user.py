from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool = True


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    id: UUID


class UserInDBBase(UserBase):
    id: UUID
    hashed_password: str

    model_config = ConfigDict(from_attributes=True)


class User(UserInDBBase):
    pass
