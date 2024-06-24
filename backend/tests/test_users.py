from http import HTTPStatus


def test_criar_usuario(client):
    response = client.post(
        '/users/',
        json={
            'username': 'fausto',
            'email': 'fausto@fausto.com',
            'senha': '1234567'
        }
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'fausto',
        'email': 'fausto@fausto.com',
        'id': 1
    }
