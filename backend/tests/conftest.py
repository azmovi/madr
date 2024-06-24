import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from mader.app import app
from mader.models import table_registry


@pytest.fixture()
def session():
    engine = create_engine("postgresql+psycopg://postgres:postgres@localhost:5432/mader_test")
    table_registry.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture()
def client(session):
    return TestClient(app)
