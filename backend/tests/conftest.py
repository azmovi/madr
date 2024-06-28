import pytest_asyncio
from faker import Faker
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from testcontainers.postgres import PostgresContainer

from mader.app import app
from mader.database import get_async_session
from mader.models import User, table_registry
from mader.utils import add_commit, sanitizar_username


@pytest_asyncio.fixture(scope='session')
async def async_engine():
    with PostgresContainer('postgres:16', driver='psycopg') as postgres:
        _engine = create_async_engine(postgres.get_connection_url())

        async with _engine.begin():
            yield _engine


@pytest_asyncio.fixture()
async def async_session(async_engine: AsyncEngine):
    async with async_engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    async with AsyncSession(
        async_engine, expire_on_commit=False
    ) as async_session:
        yield async_session

    async with async_engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)


@pytest_asyncio.fixture()
async def client(async_session: AsyncSession):
    async def get_async_session_override():
        yield async_session

    app.dependency_overrides[get_async_session] = get_async_session_override

    async with AsyncClient(app=app, base_url='http://dummy') as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture()
async def user(async_session: AsyncSession, faker: Faker) -> User:
    nome_sanitizado = sanitizar_username(faker.name())
    user = User(
        username=nome_sanitizado,
        email=faker.email(),
        senha=faker.password(),
    )
    await add_commit(user, async_session)
    return user
