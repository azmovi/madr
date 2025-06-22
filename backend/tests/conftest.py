import uuid
from collections.abc import AsyncGenerator
from contextlib import contextmanager
from datetime import datetime

import pytest
import pytest_asyncio
from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from testcontainers.postgres import PostgresContainer

from mader.app import app
from mader.database import add_obj, get_session
from mader.models import User, table_registry
from tests.factories import AdminFactory, UserFactory


@pytest_asyncio.fixture(scope='session')
async def engine():
    with PostgresContainer('postgres:latest', driver='psycopg') as postgres:
        engine = create_async_engine(postgres.get_connection_url())
        yield engine


@pytest_asyncio.fixture
async def session(engine) -> AsyncGenerator[AsyncSession]:
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@contextmanager
def _mock_db_time(*, model, time=datetime.now()):
    def fake_time_handler(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_handler)
    yield time
    event.remove(model, 'before_insert', fake_time_handler)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@contextmanager
def _mock_db_uuid(*, model, uuid=uuid.uuid4()):
    def fake_uuid_handler(mapper, connection, target):
        if hasattr(target, 'id'):
            target.id = uuid

    event.listen(model, 'before_insert', fake_uuid_handler)
    yield uuid
    event.remove(model, 'before_insert', fake_uuid_handler)


@pytest.fixture
def mock_db_uuid():
    return _mock_db_uuid


@pytest_asyncio.fixture
async def user(session: AsyncSession, faker: Faker) -> User:
    senha = faker.password()
    user = UserFactory(senha=senha)
    await add_obj(session, user)
    user.senha_limpa = senha
    return user


@pytest_asyncio.fixture
async def admin(session: AsyncSession, faker: Faker) -> User:
    senha = faker.password()
    user = AdminFactory(senha=senha)
    await add_obj(user, session)
    user.senha_limpa = senha
    return user


@pytest.fixture
def token(client: TestClient, user: User) -> str:
    response = client.post(
        '/auth/token',
        data={
            'username': user.email,
            'password': user.senha_limpa,  # type: ignore[attr-defined]
        },
    )
    return response.json()['access_token']
