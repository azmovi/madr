import pytest
from faker import Faker
from jwt import decode

from mader.security import criar_token_jwt_de_acesso
from mader.settings import settings


@pytest.mark.asyncio()
async def test_criar_token_jwt(faker: Faker):
    data = {'subject': faker.email()}
    token = await criar_token_jwt_de_acesso(data)

    decodificado = decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
    assert decodificado['exp']

    decodificado.pop('exp')
    assert decodificado == data


print(test_criar_token_jwt(Faker()))
