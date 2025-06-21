import pytest
from faker import Faker
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from mader.models import User
from mader.schemas import Role


@pytest.mark.asyncio
async def test_criar_ususario_db(session: AsyncSession, faker: Faker):
    novo_usuario = User(
        username=faker.name(),
        senha=faker.password(),
        email=faker.email(),
        role=Role.USER,
    )

    session.add(novo_usuario)
    await session.commit()

    db_user = await session.scalar(
        select(User).where(User.username == novo_usuario.username)
    )

    assert db_user
    assert db_user.username == novo_usuario.username
    assert db_user.email == novo_usuario.email
