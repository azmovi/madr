from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from mader.database import Session, add_obj, refresh_obj
from mader.models import User
from mader.schemas import Message, Role, UsuarioPublico, UsuarioSchema
from mader.security import UsuarioAutenticado

router = APIRouter(prefix='/conta', tags=['conta'])


@router.post(
    '/', response_model=UsuarioPublico, status_code=HTTPStatus.CREATED
)
async def criar_conta(usuario: UsuarioSchema, session: Session):
    try:
        db_usuario = User(
            username=usuario.username,
            email=usuario.email,
            senha=usuario.senha,
            role=Role.USER,
        )

        await add_obj(session, db_usuario)
        return db_usuario
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Conta já consta no MADR'
        )


@router.put('/{conta_id}', response_model=UsuarioPublico)
async def atualizar_conta(
    conta_id: UUID,
    user_input: UsuarioSchema,
    session: Session,
    usuario: UsuarioAutenticado,
):
    try:
        usuario.username = user_input.username
        usuario.email = user_input.email
        usuario.senha = user_input.senha
        await refresh_obj(session, usuario)

        return usuario

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Conta já consta no MADR'
        )


@router.delete('/{conta_id}', response_model=Message)
async def deletar_conta(
    conta_id: UUID, session: Session, usuario: UsuarioAutenticado
):
    await session.delete(usuario)
    await session.commit()

    return {'message': 'Conta deletada com sucesso'}


@router.get('/', response_model=list[UsuarioPublico])
async def get_contas(
    session: Session,
    limit: int = Query(default=50),
    offset: int = Query(default=0),
):
    result = await session.scalars(select(User).limit(limit).offset(offset))
    return result.all()
