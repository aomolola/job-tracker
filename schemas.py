from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class ApplicationStatus(str, Enum):
    APPLIED = "Applied"
    INTERVIEW = "Interview"
    OFFER = "Offer"
    REJECTED = "Rejected"
    WITHDRAWN = "Withdrawn"


class JobApplicationCreate(BaseModel):
    company: str = Field(min_length=1)
    position: str = Field(min_length=1)
    status: ApplicationStatus
    salary: float = Field(ge=0)
    experience: int = Field(ge=0)
    deadline: date | None = None
    notes: str | None = None
    interview_date: datetime | None = None


class JobApplicationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company: str
    position: str
    status: ApplicationStatus
    salary: float
    experience: int
    deadline: date | None = None
    notes: str | None = None
    interview_date: datetime | None = None


class JobApplicationListResponse(BaseModel):
    page: int
    limit: int
    total: int
    total_pages: int
    applications: list[JobApplicationResponse]


class JobApplicationUpdate(BaseModel):
    company: str = Field(min_length=1)
    position: str = Field(min_length=1)
    status: ApplicationStatus
    salary: float = Field(ge=0)
    experience: int = Field(ge=0)
    deadline: date | None = None
    notes: str | None = None
    interview_date: datetime | None = None


class JobApplicationUpdateResponse(BaseModel):
    message: str
    application: JobApplicationResponse