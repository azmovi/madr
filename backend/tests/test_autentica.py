from http import HTTPStatus

import pytest
from factory import Faker
from freezegun import freeze_time
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
async def test_token_para_email_inexistente(
    client: AsyncClient, user: User
):
    response = await client.post(
        '/token',
        data={'username': 'xpto' + user.email, 'password': user.senha_limpa},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email ou senha incorretos'}


@pytest.mark.asyncio()
async def test_token_senha_incorreta(
    client: AsyncClient, user: User
):
    response = await client.post(
        '/token',
        data={'username': user.email, 'password': user.senha},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email ou senha incorretos'}


@pytest.mark.asyncio()
async def test_refresh_token(
        client: AsyncClient, user: User, token: str
):
    response = await client.post(
        '/refresh-token',
        headers={'Authorization': f'Bearer {token}'},
    )

    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in data
    assert 'token_type' in data
    assert data['token_type'] == 'bearer'


@pytest.mark.asyncio()
async def test_jwt_expirou(client: AsyncClient, user: User, faker: Faker):
    with freeze_time('2024-08-10 12:00:00'):
        response = await client.post(
            '/token',
            data={'username': user.email, 'password': user.senha_limpa},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2024-08-10 13:00:01'):
        response = await client.put(
            f'/conta/{user.id}',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'username': faker.email(),
                'email': 'test@test.com',
                'senha': '',
            },
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}
