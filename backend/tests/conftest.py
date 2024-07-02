import pytest_asyncio
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
from mader.security import criptografar_senha
from mader.utils import add_commit
from tests.factories import UserFactory


@pytest_asyncio.fixture(scope='session')
async def async_engine():
    with PostgresContainer('postgres:latest', driver='psycopg') as postgres:
        _engine = create_async_engine(postgres.get_connection_url())
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
async def user(async_session: AsyncSession) -> User:
    senha_fake = 'testtest'
    user = UserFactory(senha=criptografar_senha(senha_fake))
    await add_commit(user, async_session)
    user.senha_limpa = 'testtest'
    return user


@pytest_asyncio.fixture()
async def token(client: AsyncClient, user: User) -> str:
    response = await client.post(
        '/token', data={'username': user.email, 'password': user.senha_limpa}
    )
    return response.json()['access_token']
