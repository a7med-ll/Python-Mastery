# -----------------------------------------------------------------------------
# Test Configuration
# -----------------------------------------------------------------------------

import pytest
import fakeredis

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.api.dependencies import get_database_session
from app.database.base import Base
from app.cache.redis import redis_client
from app.core.config import settings


# -----------------------------------------------------------------------------
# Isolated Test Services
# -----------------------------------------------------------------------------

test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)


Base.metadata.create_all(bind=test_engine)


redis_client.client = fakeredis.FakeRedis(
    decode_responses=True
)


settings.RATE_LIMIT_ENABLED = False


# -----------------------------------------------------------------------------
# API Test Client
# -----------------------------------------------------------------------------

@pytest.fixture
def client():

    connection = test_engine.connect()

    transaction = connection.begin()

    TestingSession = sessionmaker(
        bind=connection,
        autoflush=False,
        autocommit=False
    )


    def override_database_session():

        database = TestingSession()

        try:

            yield database

        finally:

            database.close()


    app.dependency_overrides[get_database_session] = override_database_session

    redis_client.client.flushall()


    with TestClient(app) as test_client:

        yield test_client


    app.dependency_overrides.clear()

    transaction.rollback()

    connection.close()
