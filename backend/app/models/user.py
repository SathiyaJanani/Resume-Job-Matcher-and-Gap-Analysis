"""
SQLAlchemy ORM models for Users, Candidates (Students), and Recruiters.
Maps to existing 'candidates' and 'recruiters' tables while introducing 'users'.
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from backend.app.database import Base


def now_iso():
    return datetime.now(timezone.utc).isoformat()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="STUDENT")  # 'STUDENT' or 'RECRUITER'
    created_at = Column(String(100), default=now_iso)

    # Relationships
    candidate = relationship("Candidate", back_populates="user", uselist=False)
    recruiter = relationship("Recruiter", back_populates="user", uselist=False)
    chat_sessions = relationship("ChatSession", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(50), nullable=False)
    location = Column(String(255), nullable=False)
    current_title = Column(String(255), nullable=False)
    years_experience = Column(Float, nullable=False, default=0.0)
    highest_degree = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False, default="Active")
    created_at = Column(String(100), default=now_iso)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Relationships
    user = relationship("User", back_populates="candidate")
    resumes = relationship("Resume", back_populates="candidate", cascade="all, delete-orphan")
    skills = relationship("CandidateSkill", back_populates="candidate", cascade="all, delete-orphan")
    applications = relationship("JobApplication", back_populates="candidate", cascade="all, delete-orphan")
    match_results = relationship("MatchResult", back_populates="candidate", cascade="all, delete-orphan")
    learning_recommendations = relationship("LearningRecommendation", back_populates="candidate", cascade="all, delete-orphan")


class Recruiter(Base):
    __tablename__ = "recruiters"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    role = Column(String(255), nullable=False)
    department = Column(String(255), nullable=False)
    active_requisitions = Column(Integer, nullable=False, default=0)
    phone = Column(String(50), nullable=False)
    created_at = Column(String(100), default=now_iso)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Relationships
    user = relationship("User", back_populates="recruiter")
    company = relationship("Company", back_populates="recruiters")
    jobs = relationship("Job", back_populates="recruiter", cascade="all, delete-orphan")
    applications = relationship("JobApplication", back_populates="recruiter")
    interviews = relationship("Interview", back_populates="recruiter")
