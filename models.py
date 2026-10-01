from sqlalchemy import Column, Integer, String
from database import Base


class JobApplication(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, nullable=False)
    position = Column(String, nullable=False)
    status = Column(String, nullable=False)
    salary = Column(Integer, nullable=False)
    experience = Column(Integer, nullable=False)
