import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.deps import get_db
from app.api.main import app
from app.models.base import Base

# In-memory SQLite database with StaticPool for thread-safe test sharing
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

# Attach PostgreSQL schemas for SQLite compatibility
@event.listens_for(engine, "connect")
def attach_schemas(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("ATTACH DATABASE ':memory:' AS bronze;")
    cursor.execute("ATTACH DATABASE ':memory:' AS silver;")
    cursor.execute("ATTACH DATABASE ':memory:' AS gold;")
    cursor.close()

TestingSessionLocal = sessionmaker(autoflush=False, bind=engine)

# Fixture
@pytest.fixture(scope="function")
def db_session():
    """Creates a fresh database schema for each test, yields session, and cleans up after test."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """FastAPI TestClient with overridden get_db dependency pointing to the in-memory test DB."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()