from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from mader.database import AsyncSession
from mader.models import User
from mader.schemas import Message, UsuarioPublico, UsuarioSchema
from mader.security import UsuarioAtual, criptografar_senha
from mader.utils import (
    add_commit,
    atualizar_usuario,
    atualizar_usuario_no_banco,
    sanitizar_username,
)

router = APIRouter(prefix='/conta', tags=['conta'])


@router.post(
    '/', response_model=UsuarioPublico, status_code=HTTPStatus.CREATED
)
async def criar_conta(usuario: UsuarioSchema, session: AsyncSession):
    username_sanitizado = sanitizar_username(usuario.username)

    db_usuario = await session.scalar(
        select(User).where(
            (User.email == usuario.email)
            | (User.username == username_sanitizado)
        )
    )
    if db_usuario:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Conta já consta no MADR'
        )

    senha_criptografada = criptografar_senha(usuario.senha)

    db_usuario = User(
        username=usuario.username,
        email=usuario.email,
        senha=senha_criptografada,
    )
    await add_commit(db_usuario, session)
    return db_usuario


@router.put('/{conta_id}', response_model=UsuarioPublico)
async def atualizar_conta(
    conta_id: int,
    usuario: UsuarioSchema,
    session: AsyncSession,
    usuario_atual: UsuarioAtual,
):
    if conta_id != usuario_atual.id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Permissão insuficiente'
        )
    atualizar_usuario(usuario, usuario_atual)
    await atualizar_usuario_no_banco(session, usuario_atual)

    return usuario_atual


@router.delete('/{conta_id}', response_model=Message)
async def deletar_conta(
    conta_id: int, session: AsyncSession, usuario_atual: UsuarioAtual
):
    if conta_id != usuario_atual.id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Permissão insuficiente'
        )

    await session.delete(usuario_atual)
    await session.commit()

    return {'message': 'Conta deletada com sucesso'}
