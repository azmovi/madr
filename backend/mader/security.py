from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Annotated, Any

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import DecodeError, ExpiredSignatureError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from zoneinfo import ZoneInfo

from mader.database import AsyncSession
from mader.models import User
from mader.schemas import TokenData
from mader.settings import settings

pwd_context = PasswordHash.recommended()


def criar_token_jwt_de_acesso(dados: dict[str, Any]) -> str:
    dados_para_codificar = dados.copy()
    tmp_exp = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    dados_para_codificar.update({'exp': tmp_exp})
    dados_codificados = encode(
        dados_para_codificar, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return dados_codificados


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/token')


async def get_usuario_atual(
    session: AsyncSession, token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        username: str = payload.get('sub')
        if not username:
            raise credentials_exception

        token_data = TokenData(username=username)

    except DecodeError:
        raise credentials_exception

    except ExpiredSignatureError:
        raise credentials_exception

    user_db = await session.scalar(
        select(User).where(User.email == token_data.username)
    )

    if not user_db:
        raise credentials_exception

    return user_db


def criptografar_senha(senha: str) -> str:
    return pwd_context.hash(senha)


def verificar_senha(plaintext_senha: str, hashed_senha: str) -> bool:
    return pwd_context.verify(plaintext_senha, hashed_senha)


OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
UsuarioAtual = Annotated[User, Depends(get_usuario_atual)]
