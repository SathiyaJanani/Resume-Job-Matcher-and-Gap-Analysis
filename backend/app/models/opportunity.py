"""
SQLAlchemy ORM models for Companies and Jobs (Opportunities).
Maps to existing 'companies' and 'jobs' tables.
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from backend.app.database import Base


def now_iso():
    return datetime.now(timezone.utc).isoformat()


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    industry = Column(String(255), nullable=False)
    size_range = Column(String(100), nullable=False)
    headquarters = Column(String(255), nullable=False)
    website = Column(String(255), nullable=False)
    rating = Column(Float, nullable=False, default=4.5)
    verified = Column(Integer, nullable=False, default=1)
    created_at = Column(String(100), default=now_iso)

    # Relationships
    recruiters = relationship("Recruiter", back_populates="company", cascade="all, delete-orphan")
    jobs = relationship("Job", back_populates="company", cascade="all, delete-orphan")


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    recruiter_id = Column(Integer, ForeignKey("recruiters.id"), nullable=False)
    title = Column(String(255), index=True, nullable=False)
    department = Column(String(255), nullable=False)
    employment_type = Column(String(100), nullable=False, default="Full-time")  # 'Job', 'Internship', 'Full-time'
    experience_level = Column(String(100), nullable=False)
    location_type = Column(String(100), nullable=False)
    salary_range = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String(50), nullable=False, default="Open")
    created_at = Column(String(100), default=now_iso)

    # Extended academic fields
    min_cgpa = Column(Float, nullable=True, default=6.5)
    min_experience = Column(Float, nullable=True, default=0.0)
    deadline = Column(String(100), nullable=True)

    # Relationships
    company = relationship("Company", back_populates="jobs")
    recruiter = relationship("Recruiter", back_populates="jobs")
    skills = relationship("JobSkill", back_populates="job", cascade="all, delete-orphan")
    applications = relationship("JobApplication", back_populates="job", cascade="all, delete-orphan")
    match_results = relationship("MatchResult", back_populates="job", cascade="all, delete-orphan")
