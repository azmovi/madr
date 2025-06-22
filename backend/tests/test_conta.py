from http import HTTPStatus
from uuid import uuid4

import pytest
from faker import Faker
from fastapi.testclient import TestClient

from mader.models import User
from mader.schemas import Role
from mader.utils import sanitizar_username


@pytest.mark.asyncio
async def test_criar_usuario(client: TestClient, faker: Faker, mock_db_uuid):
    username, email, senha = faker.name(), faker.email(), faker.password()
    payload = {
        'username': username,
        'email': email,
        'senha': senha,
    }
    with mock_db_uuid(model=User) as uuid:
        response = client.post('/conta/', json=payload)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': str(uuid),
        'role': Role.USER,
        'username': sanitizar_username(username),
        'email': email,
    }


def test_criar_usuario_com_username_existente(
    client: TestClient, faker: Faker, user: User
):
    response = client.post(
        '/conta/',
        json={
            'username': user.username,
            'email': faker.email(),
            'senha': faker.password(),
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Conta já consta no MADR'}


def test_criar_usuario_com_email_existente(
    client: TestClient, faker: Faker, user: User
):
    response = client.post(
        '/conta/',
        json={
            'username': faker.name(),
            'email': user.email,
            'senha': faker.password(),
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Conta já consta no MADR'}


def test_atualizar_usuario(
    client: TestClient, faker: Faker, user: User, token: str
):
    username, email, senha = faker.name(), faker.email(), faker.password()
    payload = {
        'username': username,
        'email': email,
        'senha': senha,
    }
    response = client.put(
        f'/conta/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json=payload,
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': str(user.id),
        'role': Role.USER,
        'username': sanitizar_username(username),
        'email': email,
    }


def test_atualizar_usuario_id_errado(
    client: TestClient, faker: Faker, user: User, token: str
):
    esperado = {
        'username': sanitizar_username(faker.name()),
        'email': faker.email(),
    }
    payload = {**esperado, 'senha': faker.password()}

    response = client.put(
        f'/conta/{uuid4()}',
        headers={'Authorization': f'Bearer {token}'},
        json=payload,
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Permissão insuficiente'}


def test_deletar_usuario(client: TestClient, user: User, token: str):
    response = client.delete(
        f'/conta/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Conta deletada com sucesso'}


def test_deletar_usuario_id_errado(client: TestClient, user: User, token: str):
    response = client.delete(
        f'/conta/{uuid4()}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Permissão insuficiente'}


def test_deletar_usuario_com_token_invalido(
    client: TestClient, user: User, token: str
):
    response = client.delete(
        f'/conta/{uuid4()}',
        headers={'Authorization': 'Bearer xpto'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Autenticação invalida'}


def test_get_conta_without_conta(client: TestClient):
    response = client.get('/conta')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == []


def test_get_conta(client: TestClient, user: User):
    response = client.get('/conta')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == [
        {
            'id': str(user.id),
            'role': Role.USER,
            'username': user.username,
            'email': user.email,
        }
    ]
