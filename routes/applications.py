from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import SessionLocal
from models import JobApplication as JobApplicationModel
from schemas import (
    JobApplicationCreate,
    JobApplicationResponse,
    JobApplicationListResponse,
    JobApplicationUpdate,
    JobApplicationUpdateResponse,
)


router = APIRouter(
    prefix="/applications",
    tags=["Applications"],
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post(
    "",
    response_model=JobApplicationResponse,
)
def create_application(
    application: JobApplicationCreate,
    db: Session = Depends(get_db),
):
    new_application = JobApplicationModel(
        company=application.company,
        position=application.position,
        status=application.status,
        salary=application.salary,
        experience=application.experience,
        deadline=application.deadline,
        notes=application.notes,
    )

    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return new_application


@router.get(
    "",
    response_model=JobApplicationListResponse,
)
def get_applications(
    status: str | None = None,
    company: str | None = None,
    search: str | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(JobApplicationModel)

    if status:
        query = query.filter(
            JobApplicationModel.status == status
        )

    if company:
        query = query.filter(
            JobApplicationModel.company == company
        )

    if search:
        search_term = f"%{search}%"

        query = query.filter(
            (JobApplicationModel.company.ilike(search_term))
            |
            (JobApplicationModel.position.ilike(search_term))
        )

    total = query.count()

    offset = (page - 1) * limit

    applications = (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )

    total_pages = (total + limit - 1) // limit

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
        "applications": applications,
    }


@router.get(
    "/{application_id}",
    response_model=JobApplicationResponse,
)
def get_application(
    application_id: int,
    db: Session = Depends(get_db),
):
    application = (
        db.query(JobApplicationModel)
        .filter(JobApplicationModel.id == application_id)
        .first()
    )

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found",
        )

    return application


@router.put(
    "/{application_id}",
    response_model=JobApplicationUpdateResponse,
)
def update_application(
    application_id: int,
    update: JobApplicationUpdate,
    db: Session = Depends(get_db),
):
    application = (
        db.query(JobApplicationModel)
        .filter(JobApplicationModel.id == application_id)
        .first()
    )

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found",
        )

    application.company = update.company
    application.position = update.position
    application.status = update.status
    application.salary = update.salary
    application.experience = update.experience
    application.deadline = update.deadline
    application.notes = update.notes

    db.commit()
    db.refresh(application)

    return {
        "message": "Application successfully updated",
        "application": application,
    }


@router.delete(
    "/{application_id}",
)
def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
):
    application = (
        db.query(JobApplicationModel)
        .filter(JobApplicationModel.id == application_id)
        .first()
    )

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found",
        )

    db.delete(application)
    db.commit()

    return {
        "message": "Application deleted successfully",
    }



def test_create_application_with_deadline():
    response = client.post(
        "/applications",
        json={
            "company": "Pytest Test Company",
            "position": "Software Engineer",
            "status": "Applied",
            "salary": 95000,
            "experience": 1,
            "deadline": "2026-10-15",
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["company"] == "Pytest Test Company"
    assert data["deadline"] == "2026-10-15"