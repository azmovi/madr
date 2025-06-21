from http import HTTPStatus

import pytest
from faker import Faker
from fastapi import HTTPException
from fastapi.testclient import TestClient
from jwt import decode, encode
from sqlalchemy.ext.asyncio import AsyncSession

from mader.models import User
from mader.security import criar_token_jwt_de_acesso, get_usuario_atual
from mader.settings import settings


def test_criar_token_jwt():
    data = {'subject': 'test'}
    token = criar_token_jwt_de_acesso(data)

    decodificado = decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
    assert decodificado['subject'] == data['subject']
    assert decodificado['exp']


def test_token_jwt_invalido(client: TestClient, user: User):
    response = client.delete(
        f'/conta/{user.id}', headers={'Authorization': 'Bearer token-invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


@pytest.mark.asyncio
async def test_token_sub_vazio(session: AsyncSession):
    token = encode({}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    with pytest.raises(HTTPException) as excinfo:
        await get_usuario_atual(session=session, token=token)

    assert excinfo.value.status_code == HTTPStatus.UNAUTHORIZED
    assert excinfo.value.detail == 'Could not validate credentials'


@pytest.mark.asyncio
async def test_token_usuario_inexistente(session: AsyncSession, faker: Faker):
    token = encode(
        {'sub': faker.email()},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    with pytest.raises(HTTPException) as excinfo:
        await get_usuario_atual(session=session, token=token)

    assert excinfo.value.status_code == HTTPStatus.UNAUTHORIZED
    assert excinfo.value.detail == 'Could not validate credentials'
