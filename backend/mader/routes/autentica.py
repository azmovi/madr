from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from mader.database import AsyncSession
from mader.models import User
from mader.schemas import Token
from mader.security import (
    OAuth2Form,
    criar_token_jwt_de_acesso,
    verificar_senha,
)

router = APIRouter(prefix='', tags=[])


@router.post('/token', status_code=HTTPStatus.OK, response_model=Token)
async def conseguir_token(credenciais: OAuth2Form, session: AsyncSession):
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

    token = await criar_token_jwt_de_acesso({'sub': db_user.email})

    return {'access_token': token, 'token_type': 'bearer'}
