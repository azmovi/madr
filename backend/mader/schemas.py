import uuid
from enum import IntEnum, auto

from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class UsuarioSchema(BaseModel):
    username: str
    email: EmailStr
    senha: str


class Role(IntEnum):
    ADMIN = auto()
    USER = auto()


class UsuarioPublico(BaseModel):
    id: uuid.UUID
    username: str
    email: EmailStr
    role: Role


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
