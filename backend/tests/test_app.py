from http import HTTPStatus


def test_retornar_ola_mundo_e_ok(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Ola mundo'}
