from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from App.main import app
from App.database import get_db
from App import Models, Schemas
from .payloads import *
################################################################################

TEST_DB_URL = "sqlite:///C:/Dev/Python/FroggeAPIv3/Tests/testing-db.sqlite"

engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

################################################################################
@pytest.fixture(scope="session")
def setup_db():
    """Create and drop all tables once per test session."""

    Models.BaseModel.metadata.drop_all(bind=engine)
    Models.BaseModel.metadata.create_all(bind=engine)
    yield

################################################################################
@pytest.fixture(scope="session")
def session_client(setup_db):
    """Session-scoped client used only for initial setup tasks."""

    TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def _override_get_db():
        db = TestingSession()
        try:
            yield db
            db.commit()
        finally:
            db.close()

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

################################################################################
@pytest.fixture(scope="session", autouse=True)
def make_master_session_records(session_client):
    """Create a guild, register a user, and login at once for all tests."""

    res = session_client.post(f"/guilds/", json=GUILD_ID_PAYLOAD)
    assert res.status_code == 201, f"Guild creation failed: {res.json()}"

    res = session_client.post("/auth/register", json=REGISTER_CLIENT_PAYLOAD)
    assert res.status_code == 201, f"User registration failed: {res.json()}"

################################################################################
@pytest.fixture(scope="session")
def login_header(session_client):
    """Login fixture to get access token for authenticated requests."""

    res = session_client.post("/auth/login", data=LOGIN_FORM_DATA)
    assert res.status_code == 200, f"Login failed: {res.json()}"
    result = res.json()
    assert "access_token" in result, "Login response should contain access token"
    assert "token_type" in result, "Login response should contain token type"
    assert result["token_type"] == "bearer", "Token type should be 'bearer'"
    yield {"Authorization": f"Bearer {result['access_token']}"}

################################################################################
@pytest.fixture(scope="function")
def db_session():
    """Provide a fresh database session for each test."""

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()

################################################################################
@pytest.fixture(scope="function")
def client(db_session, login_header):
    """FastAPI test client with overridden database dependency."""

    def _override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as c:
        c.headers.update(login_header)
        c.headers.update({"X-Actor-Id": str(TEST_USER_ID)})
        yield c
    app.dependency_overrides.clear()

################################################################################
