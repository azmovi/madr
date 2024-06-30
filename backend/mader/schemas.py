from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class UsuarioSchema(BaseModel):
    username: str
    email: EmailStr
    senha: str


class UsuarioPublico(BaseModel):
    id: int
    username: str
    email: EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
