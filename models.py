
from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)


class JobApplication(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    company = Column(String, nullable=False)
    position = Column(String, nullable=False)
    status = Column(String, nullable=False)
    salary = Column(Integer, nullable=False)
    experience = Column(Integer, nullable=False)
    deadline = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)
    interview_date = Column(Date, nullable=True)
