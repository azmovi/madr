from http import HTTPStatus

from factory import Faker
from fastapi.testclient import TestClient
from freezegun import freeze_time

from mader.models import User


def test_conseguir_token_de_acesso(client: TestClient, user: User):
    response = client.post(
        '/token', data={'username': user.email, 'password': user.senha_limpa}
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


def test_token_para_email_inexistente(client: TestClient, user: User):
    response = client.post(
        '/token',
        data={'username': 'xpto' + user.email, 'password': user.senha_limpa},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email ou senha incorretos'}


def test_token_senha_incorreta(client: TestClient, user: User):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.senha},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email ou senha incorretos'}


def test_refresh_token(client: TestClient, user: User, token: str):
    response = client.post(
        '/refresh-token',
        headers={'Authorization': f'Bearer {token}'},
    )

    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in data
    assert 'token_type' in data
    assert data['token_type'] == 'bearer'


def test_jwt_expirou(client: TestClient, user: User, faker: Faker):
    with freeze_time('2024-08-10 12:00:00'):
        response = client.post(
            '/token',
            data={'username': user.email, 'password': user.senha_limpa},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2024-08-10 13:00:01'):
        response = client.put(
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
