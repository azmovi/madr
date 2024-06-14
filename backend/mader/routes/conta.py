from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from mader.database import get_session
from mader.models import User
from mader.schemas import UsuarioPublico, UsuarioSchema
from mader.utils import sanitizar_username

router = APIRouter(prefix='/conta', tags=['conta'])
Session = Annotated[Session, Depends(get_session)]


@router.post(
    '/', response_model=UsuarioPublico, status_code=HTTPStatus.CREATED
)
async def criar_conta(usuario: UsuarioSchema, session: Session):
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
    # senha_criptografada = criptografar_senha(usuario.senha)
    return db_usuario
