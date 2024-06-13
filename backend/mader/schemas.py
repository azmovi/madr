from pydantic import BaseModel


class Message(BaseModel):
    detail: str


class UsuarioSchema(BaseModel):
    id: int
    username: str
    email: str
    senha: str


class UsuarioPublico(BaseModel):
    id: int
    username: str
    email: str
    senha: str
