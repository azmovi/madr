from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from mader.database import Session
from mader.models import User
from mader.schemas import Token
from mader.security import (
    OAuth2Form,
    UsuarioAtual,
    criar_token_jwt_de_acesso,
)
from mader.utils import verificar_senha

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/token', response_model=Token)
async def get_token(
    credenciais: OAuth2Form, session: Session
) -> dict[str, str]:
    credenciais_invalidas = HTTPException(
        status_code=HTTPStatus.BAD_REQUEST, detail='Email ou senha incorretos'
    )
    if not (
        db_user := await session.scalar(
            select(User).where(User.email == credenciais.username)
        )
    ):
        raise credenciais_invalidas

    if not verificar_senha(credenciais.password, db_user.senha):
        raise credenciais_invalidas

    token = criar_token_jwt_de_acesso({
        'sub': db_user.email,
        'role': db_user.role,
    })

    return {'access_token': token, 'token_type': 'bearer'}


@router.post('/refresh-token', response_model=Token)
async def refresh_token(user: UsuarioAtual) -> dict[str, str]:
    token_atualizado = criar_token_jwt_de_acesso({
        'sub': user.email,
        'role': user.role,
    })

    return {'access_token': token_atualizado, 'token_type': 'bearer'}
