from http import HTTPStatus

from fastapi.testclient import TestClient


def test_retornar_ola_mundo_e_ok(client: TestClient):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Ola mundo'}
