from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import SessionLocal
from models import JobApplication as JobApplicationModel
from schemas import (
    JobApplicationCreate,
    JobApplicationUpdate,
    JobApplicationResponse,
    JobApplicationUpdateResponse,
    JobApplicationListResponse
)
from routes.applications import router as applications_router



app = FastAPI(
    title="Job Application Tracker API",
    description="A REST API for tracking and managing job appliations.",
    version="1.0.0"
)

app.include_router(applications_router)


# Database dependency
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

# Home
@app.get("/")
def home():
    return {
        "message": "Job Tracker API is running!"
    }


# Health check
@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


# About
@app.get("/about")
def about():
    return {
        "project": "Job Application Tracker",
        "version": "1.0"
    }


# Database test
@app.get("/db-test")
def database_test(db: Session = Depends(get_db)):
    return {
        "message": "Database connection successful!"
    }
