from http import HTTPStatus

import pytest


@pytest.mark.asyncio()
async def test_retornar_ola_mundo_e_ok(client):
    response = await client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Ola mundo'}
