import pytest
from faker import Faker
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from mader.models import User


@pytest.mark.asyncio
async def test_criar_ususario_db(async_session: AsyncSession, faker: Faker):
    novo_usuario = User(
        username=faker.name(), senha=faker.password(), email=faker.email()
    )

    async_session.add(novo_usuario)
    await async_session.commit()

    db_user = await async_session.scalar(
        select(User).where(User.username == novo_usuario.username)
    )

    assert db_user
    assert db_user.username == novo_usuario.username
    assert db_user.email == novo_usuario.email
