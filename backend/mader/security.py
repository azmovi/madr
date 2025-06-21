from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Annotated, Any
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import DecodeError, ExpiredSignatureError, decode, encode
from sqlalchemy import select

from mader.database import Session
from mader.exceptions import credentials_exception
from mader.models import User
from mader.schemas import Role, TokenData
from mader.settings import settings


def criar_token_jwt_de_acesso(dados: dict[str, Any]) -> str:
    tmp_exp = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return encode(
        dados.copy() | {'exp': tmp_exp},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='auth/token', refreshUrl='auth/refresh-token'
)


async def get_usuario_atual(
    session: Session, token: str = Depends(oauth2_scheme)
) -> User:
    try:
        payload = decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username = payload['sub']
        token_data = TokenData(username=username)

        user_db = await session.scalar(
            select(User).where(User.email == token_data.username)
        )

        if not user_db:
            raise credentials_exception
        return user_db

    except (KeyError, DecodeError, ExpiredSignatureError):
        raise credentials_exception


UsuarioAtual = Annotated[User, Depends(get_usuario_atual)]
OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]


def get_user_with_auth(permission: Role):
    def check_role(conta_id: int, usuario_atual: UsuarioAtual) -> User:
        valid_permission = usuario_atual.role <= permission
        same_user = (
            usuario_atual.role == Role.USER and conta_id == usuario_atual.id
        )
        if not valid_permission or not same_user:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail='Permissão insuficiente'
            )
        return usuario_atual
    return check_role


UsuarioAutenticado = Annotated[User, Depends(get_user_with_auth(Role.USER))]
AdminAutenticado = Annotated[User, Depends(get_user_with_auth(Role.ADMIN))]
