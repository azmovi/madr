from http import HTTPStatus

import pytest
from faker import Faker
from httpx import AsyncClient

from mader.models import User
from mader.utils import sanitizar_username


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


@pytest.mark.asyncio()
async def test_atualizar_usuario(
    client: AsyncClient, faker: Faker, user: User, token: str
):
    esperado = {
        'username': sanitizar_username(faker.name()),
        'email': faker.email(),
    }
    payload = {**esperado, 'senha': faker.password()}

    response = await client.put(
        f'/conta/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json=payload,
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'id': user.id, **esperado}


@pytest.mark.asyncio()
async def test_atualizar_usuario_id_errado(
    client: AsyncClient, faker: Faker, user: User, token: str
):
    esperado = {
        'username': sanitizar_username(faker.name()),
        'email': faker.email(),
    }
    payload = {**esperado, 'senha': faker.password()}

    response = await client.put(
        f'/conta/{user.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
        json=payload,
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Permissão insuficiente'}


@pytest.mark.asyncio()
async def test_deletar_usuario(client: AsyncClient, user: User, token: str):
    response = await client.delete(
        f'/conta/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Conta deletada com sucesso'}


@pytest.mark.asyncio()
async def test_deletar_usuario_id_errado(
    client: AsyncClient, user: User, token: str
):
    response = await client.delete(
        f'/conta/{user.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Permissão insuficiente'}
