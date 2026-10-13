
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import SessionLocal
from routes.applications import router as applications_router
from auth.routes import router as auth_router


app = FastAPI(
    title="Job Application Tracker API",
    description="A REST API for tracking and managing job applications.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(applications_router)
app.include_router(auth_router)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {
        "message": "Job Tracker API is running!"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.get("/about")
def about():
    return {
        "project": "Job Application Tracker",
        "version": "1.0"
    }


@app.get("/db-test")
def database_test(db: Session = Depends(get_db)):
    return {
        "message": "Database connection successful!"
    }
