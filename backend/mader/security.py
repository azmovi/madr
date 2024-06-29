from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from jwt import encode
from pwdlib import PasswordHash
from zoneinfo import ZoneInfo

from mader.settings import settings

pwd_context = PasswordHash.recommended()


async def criar_token_jwt_de_acesso(dados: dict):
    dados_para_codificar = dados.copy()
    tmp_exp = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    dados_para_codificar.update({'exp': tmp_exp})
    dados_codificados = encode(
        dados_para_codificar, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return dados_codificados


def criptografar_senha(senha: str) -> str:
    return pwd_context.hash(senha)


def verificar_senha(plaintext_senha: str, hashed_senha: str) -> bool:
    return pwd_context.verify(plaintext_senha, hashed_senha)


OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
