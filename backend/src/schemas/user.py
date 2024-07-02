# type: ignore
"""Schemas das informações de usuários."""

from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, StringConstraints

UserPassword = Annotated[str, StringConstraints(min_length=8, max_length=64)]


class UserBase(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    course: Optional[str] = None


class UserCreate(UserBase):
    name: str
    email: EmailStr
    course: str
    password: UserPassword


class UserInDbBase(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class User(UserInDbBase):
    name: str
    email: str
    course: str
