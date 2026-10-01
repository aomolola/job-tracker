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
    salary: int = Field(ge=0)
    experience: int = Field(ge=0)


class JobApplicationUpdate(BaseModel):
    company: str = Field(min_length=1)
    position: str = Field(min_length=1)
    status: ApplicationStatus
    salary: int = Field(ge=0)
    experience: int = Field(ge=0)


class JobApplicationResponse(BaseModel):
    id: int
    company: str
    position: str
    status: ApplicationStatus
    salary: int
    experience: int

    model_config = ConfigDict(from_attributes=True)


class JobApplicationUpdateResponse(BaseModel):
    message: str
    application: JobApplicationResponse


class JobApplicationListResponse(BaseModel):
    page: int
    limit: int
    total: int
    total_pages: int
    applications: list[JobApplicationResponse]