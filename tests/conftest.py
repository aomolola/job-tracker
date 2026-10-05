import pytest

from database import SessionLocal
from models import JobApplication


@pytest.fixture(autouse=True)
def cleanup_test_data():
    db = SessionLocal()

    db.query(JobApplication).filter(
        JobApplication.company == "Pytest Test Company"
    ).delete()

    db.commit()
    db.close()

    yield

    db = SessionLocal()

    db.query(JobApplication).filter(
        JobApplication.company == "Pytest Test Company"
    ).delete()

    db.commit()
    db.close()
