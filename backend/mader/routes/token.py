from http import HTTPStatus

from fastapi import APIRouter
from sqlalchemy import select

from mader.database import Session
from mader.exceptions import invalid_credentials
from mader.models import User
from mader.schemas import Token
from mader.security import (
    OAuth2Form,
    UsuarioAtual,
    criar_token_jwt,
)
from mader.utils import verificar_senha

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post(
    '/token',
    response_model=Token,
    responses={
        HTTPStatus.CREATED: {'description': 'token criado com succeso'},
        HTTPStatus.BAD_REQUEST: {'description': 'Email ou senha incorretos'},
    },
)
async def create_token(
    credenciais: OAuth2Form, session: Session
) -> dict[str, str]:
    try:
        db_user = await session.scalar(
            select(User).where(User.email == credenciais.username)
        )
        verificar_senha(credenciais.password, db_user.senha)

        token = criar_token_jwt({
            'sub': str(db_user.id),
            'role': db_user.role,
        })
        return {'access_token': token, 'token_type': 'bearer'}

    except (AttributeError, ValueError):
        raise invalid_credentials


@router.post('/refresh-token', response_model=Token)
async def refresh_token(user: UsuarioAtual) -> dict[str, str]:
    token_atualizado = criar_token_jwt({
        'sub': str(user.id),
        'role': user.role,
    })

    return {'access_token': token_atualizado, 'token_type': 'bearer'}
