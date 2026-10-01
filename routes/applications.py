from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import SessionLocal
from models import JobApplication as JobApplicationModel
from schemas import JobApplicationCreate, JobApplicationResponse , JobApplicationListResponse , JobApplicationUpdate, JobApplicationUpdateResponse


router = APIRouter(
    prefix="/applications",
    tags=["Applications"]
)


# Database dependency
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# Create application # Create application
@router.post(
    "/applications",
    response_model=JobApplicationResponse,
    tags=["Applications"]
    
)
def create_application(
    application: JobApplicationCreate,
    db: Session = Depends(get_db)
):
    try:
        new_application = JobApplicationModel(
            company=application.company,
            position=application.position,
            status=application.status,
            salary=application.salary,
            experience=application.experience
        )

        db.add(new_application)
        db.commit()
        db.refresh(new_application)

        return new_application

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Failed to create application"
        )

# Get applications
# Supports:
# /applications
# /applications?status=Interview
# /applications?company=Microsoft
# /applications?search=developer
# /applications?page=1&limit=10
@router.get(
    "/applications",
    response_model=JobApplicationListResponse,
    tags=['Applications']
)
def get_applications(
    status: str | None = None,
    company: str | None = None,
    search: str | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(JobApplicationModel)

    # Filter by status
    if status:
        query = query.filter(
            JobApplicationModel.status == status
        )

    # Filter by company
    if company:
        query = query.filter(
            JobApplicationModel.company == company
        )

    # Search company or position
    if search:
        search_term = f"%{search}%"

        query = query.filter(
            (JobApplicationModel.company.ilike(search_term))
            |
            (JobApplicationModel.position.ilike(search_term))
        )

    # Total matching applications
    total = query.count()

    # Pagination
    offset = (page - 1) * limit

    applications = (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )

    # Calculate total pages
    total_pages = (total + limit - 1) // limit

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
        "applications": applications
    }



# Get one application by ID
@router.get(
    "/applications/{application_id}",
    response_model=JobApplicationResponse,
    tags=['Applications']

)
def get_application(
    application_id: int,
    db: Session = Depends(get_db)
):
    application = db.query(JobApplicationModel).filter(
        JobApplicationModel.id == application_id
    ).first()

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    return application


# Delete an application by ID
@router.delete("/applications/{application_id}",
            tags=["Applications"])
def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
):
    application = db.query(JobApplicationModel).filter(
        JobApplicationModel.id == application_id
    ).first()

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    db.delete(application)
    db.commit()

    return {
        "message": "Application deleted successfully"
    }


# Update an application by ID
@router.put(
    "/applications/{application_id}",
    response_model=JobApplicationUpdateResponse, 
    tags=["Applications"]
)
def update_application(
    application_id: int,
    update: JobApplicationUpdate,
    db: Session = Depends(get_db)
):
    application = db.query(JobApplicationModel).filter(
        JobApplicationModel.id == application_id
    ).first()

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    application.company = update.company
    application.position = update.position
    application.status = update.status
    application.salary = update.salary
    application.experience = update.experience

    db.commit()
    db.refresh(application)

    return {
        "message": "Application successfully updated",
        "application": application
    }

