from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select

from mader.database import Session
from mader.models import User
from mader.schemas import Token
from mader.security import (
    OAuth2Form,
    criar_token_jwt_de_acesso,
    get_usuario_atual,
    verificar_senha,
)

router = APIRouter(prefix='', tags=[])


@router.post('/token', response_model=Token)
async def conseguir_token(
    credenciais: OAuth2Form,
    session: Session,
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

    token = criar_token_jwt_de_acesso({'sub': db_user.email})

    return {'access_token': token, 'token_type': 'bearer'}


@router.post('/refresh-token', response_model=Token)
async def recarregar_token(
    user: User = Depends(get_usuario_atual),
) -> dict[str, str]:
    token_atualizado = criar_token_jwt_de_acesso({'sub': user.email})

    return {'access_token': token_atualizado, 'token_type': 'bearer'}
