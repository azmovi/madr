from http import HTTPStatus

import pytest
from faker import Faker
from httpx import AsyncClient

from mader.models import User


@pytest.mark.asyncio()
async def test_conseguir_token_de_acesso(client: AsyncClient, user: User):
    response = await client.post(
        '/token', data={'username': user.email, 'password': user.senha_limpa}
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


@pytest.mark.asyncio()
async def test_token_para_usuario_inexistente(
    client: AsyncClient, faker: Faker
):
    response = await client.post(
        '/token',
        data={'username': faker.email(), 'password': faker.password()},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email ou senha incorretos'}


@pytest.mark.asyncio()
async def test_token_senha_incorreta(
    client: AsyncClient, user: User, faker: Faker
):
    response = await client.post(
        '/token',
        data={'username': user.email, 'password': faker.password()},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email ou senha incorretos'}
