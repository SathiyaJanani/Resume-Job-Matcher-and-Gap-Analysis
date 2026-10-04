"""
SQLAlchemy ORM models for Resumes, MatchResults, and SkillGapReports.
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from backend.app.database import Base


def now_iso():
    return datetime.now(timezone.utc).isoformat()


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_size_kb = Column(Integer, nullable=False, default=100)
    raw_text = Column(Text, nullable=False)
    parsed_summary = Column(Text, nullable=False)
    ai_detected_seniority = Column(String(100), nullable=False, default="Mid-Level")
    uploaded_at = Column(String(100), default=now_iso)

    # Extended structured JSON fields
    education_json = Column(Text, nullable=True)
    projects_json = Column(Text, nullable=True)
    certifications_json = Column(Text, nullable=True)
    links_json = Column(Text, nullable=True)

    candidate = relationship("Candidate", back_populates="resumes")


class MatchResult(Base):
    __tablename__ = "match_results"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    match_score = Column(Float, nullable=False)
    semantic_similarity = Column(Float, nullable=False)
    skill_overlap_score = Column(Float, nullable=False)
    readiness_percentage = Column(Float, nullable=False)
    matched_skills = Column(Text, nullable=False)
    missing_skills = Column(Text, nullable=False)
    ai_summary = Column(Text, nullable=False)
    created_at = Column(String(100), default=now_iso)

    # Extended academic component scores
    experience_score = Column(Float, nullable=True, default=80.0)
    eligibility_score = Column(Float, nullable=True, default=100.0)
    eligibility_status = Column(String(50), nullable=True, default="Eligible")

    candidate = relationship("Candidate", back_populates="match_results")
    job = relationship("Job", back_populates="match_results")


class SkillGapReport(Base):
    __tablename__ = "skill_gap_reports"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=True)
    role_id = Column(Integer, nullable=True)
    matched_json = Column(Text, nullable=False)
    partially_matched_json = Column(Text, nullable=False)
    missing_json = Column(Text, nullable=False)
    roadmap_json = Column(Text, nullable=False)
    created_at = Column(String(100), default=now_iso)
