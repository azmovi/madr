from typing import AsyncGenerator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import (
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


@pytest_asyncio.fixture
async def async_session(async_engine) -> AsyncGenerator[AsyncSession]:
    async with async_engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    async with AsyncSession(async_engine, expire_on_commit=False) as session:
        yield session

    async with async_engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)


@pytest.fixture
def client(async_session):
    def get_session_override():
        return async_session

    with TestClient(app) as client:
        app.dependency_overrides[get_async_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def user(async_session: AsyncSession) -> User:
    senha_fake = 'testtest'
    user = UserFactory(senha=criptografar_senha(senha_fake))
    await add_commit(user, async_session)
    user.senha_limpa = 'testtest'
    return user


@pytest.fixture
def token(client: TestClient, user: User) -> str:
    response = client.post(
        '/token', data={'username': user.email, 'password': user.senha_limpa}
    )
    return response.json()['access_token']
