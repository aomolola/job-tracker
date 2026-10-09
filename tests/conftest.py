
import os

import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

load_dotenv()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

if not TEST_DATABASE_URL:
    raise RuntimeError(
        "TEST_DATABASE_URL is missing from .env. "
        "Tests cannot run safely without a separate test database."
    )

database_name = make_url(TEST_DATABASE_URL).database

if database_name != "job_tracker_test":
    raise RuntimeError(
        "Safety check failed: TEST_DATABASE_URL must point "
        "to job_tracker_test."
    )

test_engine = create_engine(TEST_DATABASE_URL)

TestSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)

from database import Base
from models import JobApplication, User
from main import app
import main
import auth.dependencies as auth_dependencies
import auth.routes as auth_routes
import routes.applications as applications_routes


# Create tables only in the dedicated test database.
Base.metadata.create_all(bind=test_engine)


def override_get_db():
    """Give API requests a session connected to the test database."""
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Redirect every database dependency to the test database.
app.dependency_overrides[main.get_db] = override_get_db
app.dependency_overrides[auth_dependencies.get_db] = override_get_db
app.dependency_overrides[auth_routes.get_db] = override_get_db
app.dependency_overrides[applications_routes.get_db] = override_get_db


@pytest.fixture(autouse=True)
def cleanup_test_data():
    """Clean only the isolated test database before and after each test."""

    def clear_test_database():
        with TestSessionLocal() as db:
            # Delete applications first because they reference users.
            db.query(JobApplication).delete(synchronize_session=False)
            db.query(User).delete(synchronize_session=False)
            db.commit()

    clear_test_database()
    yield
    clear_test_database()


@pytest.fixture
def app_client():
    """Provide an authenticated client for application endpoint tests."""

    with TestClient(app) as client:
        registration = client.post(
            "/api/v1/auth/register",
            json={
                "email": "applications-test@example.com",
                "password": "secure-test-password",
            },
        )

        assert registration.status_code == 201, (
            f"Test user registration failed: {registration.text}"
        )

        login = client.post(
            "/api/v1/auth/login",
            data={
                "username": "applications-test@example.com",
                "password": "secure-test-password",
            },
        )

        assert login.status_code == 200, (
            f"Test user login failed: {login.text}"
        )

        token = login.json()["access_token"]
        client.headers.update(
            {"Authorization": f"Bearer {token}"}
        )

        yield client
