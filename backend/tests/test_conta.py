from http import HTTPStatus

import pytest
from faker import Faker
from httpx import AsyncClient

from mader.models import User


@pytest.mark.asyncio()
async def test_criar_usuario(client: AsyncClient, faker: Faker):
    esperado = {'username': faker.name(), 'email': faker.email()}
    payload = {**esperado, 'senha': faker.password()}

    response = await client.post('/conta/', json=payload)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'id': 1, **esperado}


@pytest.mark.asyncio()
async def test_criar_usuario_com_username_existente(
    client: AsyncClient, faker: Faker, user: User
):
    response = await client.post(
        '/conta/',
        json={
            'username': user.username,
            'email': faker.email(),
            'senha': faker.password(),
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Conta já consta no MADR'}


@pytest.mark.asyncio()
async def test_criar_usuario_com_email_existente(
    client: AsyncClient, faker: Faker, user: User
):
    response = await client.post(
        '/conta/',
        json={
            'username': faker.name(),
            'email': user.email,
            'senha': faker.password(),
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Conta já consta no MADR'}
