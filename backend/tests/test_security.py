from faker import Faker
from jwt import decode

from mader.security import criar_token_jwt_de_acesso
from mader.settings import settings


def test_criar_token_jwt(faker: Faker):
    data = {'subject': faker.email()}
    token = criar_token_jwt_de_acesso(data)

    decodificado = decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
    assert decodificado['exp']

    decodificado.pop('exp')
    assert decodificado == data
