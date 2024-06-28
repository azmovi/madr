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
