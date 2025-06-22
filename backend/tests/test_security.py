from http import HTTPStatus

import pytest
from faker import Faker
from fastapi import HTTPException
from freezegun import freeze_time
from jwt import decode, encode
from sqlalchemy.ext.asyncio import AsyncSession

from mader.models import User
from mader.schemas import Role, Token
from mader.security import criar_token_jwt, get_usuario_atual
from mader.settings import settings


def test_criar_token_jwt():
    data = {'test': 'test'}

    token = criar_token_jwt(data)

    decodificado = decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
    assert decodificado['test'] == data['test']
    assert decodificado['exp']


@pytest.mark.asyncio
async def test_get_usuario_atual(
    session: AsyncSession, user: User, token: Token
):
    usuario_atual = await get_usuario_atual(session=session, token=token)
    assert usuario_atual == user


@pytest.mark.asyncio
async def test_token_sub_vazio(session: AsyncSession):
    token = encode({}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    with pytest.raises(HTTPException) as excinfo:
        await get_usuario_atual(session=session, token=token)

    assert excinfo.value.status_code == HTTPStatus.UNAUTHORIZED
    assert excinfo.value.detail == 'Autenticação invalida'


@pytest.mark.asyncio
async def test_token_usuario_inexistente(session: AsyncSession, faker: Faker):
    token = criar_token_jwt({'sub': faker.uuid4(), 'role': Role.USER})

    with pytest.raises(HTTPException) as error:
        await get_usuario_atual(session=session, token=token)

    assert error.value.status_code == HTTPStatus.UNAUTHORIZED
    assert error.value.detail == 'Autenticação invalida'


@pytest.mark.asyncio
async def test_token_com_tempo_expirado(session: AsyncSession, user: User):
    with freeze_time('2024-08-10 12:00:00'):
        token = criar_token_jwt({'sub': str(user.id), 'role': user.role})

    with freeze_time('2024-08-10 12:31:00'):
        with pytest.raises(HTTPException) as error:
            await get_usuario_atual(session=session, token=token)

    assert error.value.status_code == HTTPStatus.UNAUTHORIZED
    assert error.value.detail == 'Autenticação invalida'
