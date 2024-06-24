from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from mader.database import get_session
from mader.models import User
from mader.schemas import UsuarioPublico, UsuarioSchema
from mader.security import criptografar_senha
from mader.utils import sanitizar_username

router = APIRouter(prefix='/conta', tags=['conta'])
AsyncSession = Annotated[AsyncSession, Depends(get_session)]


@router.post(
    '/', response_model=UsuarioPublico, status_code=HTTPStatus.CREATED
)
async def criar_conta(usuario: UsuarioSchema, session: AsyncSession):
    username_sanitizado = sanitizar_username(usuario.username)
    db_usuario = await session.scalar(
        select(User).where(
            or_(
                User.email == usuario.email,
                User.username == username_sanitizado,
            )
        )
    )
    if db_usuario:
        return HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Conta já consta no MADR'
        )
    senha_criptografada = criptografar_senha(usuario.senha)
    db_usuario = User(
        email=usuario.email,
        username=usuario.username,
        senha=senha_criptografada
    )
    session.add(db_usuario)
    await session.commit()
    await session.refresh(db_usuario)
    return db_usuario
