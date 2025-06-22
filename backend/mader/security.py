from datetime import datetime, timedelta
from typing import Annotated
from uuid import UUID
from zoneinfo import ZoneInfo

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import decode, encode

from mader.database import Session
from mader.exceptions import insufficient_credentials, unauthorized_credentials
from mader.models import User
from mader.schemas import Role
from mader.settings import settings


def criar_token_jwt(dados: dict[str, str]) -> str:
    tmp_exp = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return encode(
        dados.copy() | {'exp': tmp_exp},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
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
        user_id = payload['sub']
        user_db = await session.get(User, user_id)

    except Exception:
        raise unauthorized_credentials

    if not user_db:
        raise unauthorized_credentials
    return user_db


UsuarioAtual = Annotated[User, Depends(get_usuario_atual)]
OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]


def get_user_with_auth(permission: Role):
    def check_role(conta_id: UUID, usuario_atual: UsuarioAtual) -> User:
        valid_permission = usuario_atual.role <= permission
        same_user = (
            usuario_atual.role == Role.USER and conta_id == usuario_atual.id
        )
        if not valid_permission or not same_user:
            raise insufficient_credentials
        return usuario_atual

    return check_role


UsuarioAutenticado = Annotated[User, Depends(get_user_with_auth(Role.USER))]
AdminAutenticado = Annotated[User, Depends(get_user_with_auth(Role.ADMIN))]
