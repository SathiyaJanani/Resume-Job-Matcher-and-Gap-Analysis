"""
SQLAlchemy ORM models for Skills taxonomy, Skill Aliases, Candidate Skills, and Job Skills.
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from backend.app.database import Base


def now_iso():
    return datetime.now(timezone.utc).isoformat()


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    skill_name = Column(String(255), unique=True, index=True, nullable=False)
    category = Column(String(100), index=True, nullable=False)
    demand_score = Column(Integer, nullable=False, default=80)
    popularity_level = Column(String(50), nullable=False, default="High")
    difficulty_level = Column(String(50), nullable=True, default="Intermediate")
    created_at = Column(String(100), default=now_iso)

    # Relationships
    aliases = relationship("SkillAlias", back_populates="skill", cascade="all, delete-orphan")
    candidate_skills = relationship("CandidateSkill", back_populates="skill", cascade="all, delete-orphan")
    job_skills = relationship("JobSkill", back_populates="skill", cascade="all, delete-orphan")
    learning_recommendations = relationship("LearningRecommendation", back_populates="skill")


class SkillAlias(Base):
    __tablename__ = "skill_aliases"

    id = Column(Integer, primary_key=True, index=True)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    alias_name = Column(String(255), unique=True, index=True, nullable=False)

    skill = relationship("Skill", back_populates="aliases")


class CandidateSkill(Base):
    __tablename__ = "candidate_skills"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    proficiency_level = Column(String(50), nullable=False, default="Intermediate")
    years_experience = Column(Float, nullable=False, default=1.0)
    verified = Column(Integer, nullable=False, default=1)
    created_at = Column(String(100), default=now_iso)

    __table_args__ = (UniqueConstraint("candidate_id", "skill_id", name="uq_candidate_skill"),)

    candidate = relationship("Candidate", back_populates="skills")
    skill = relationship("Skill", back_populates="candidate_skills")


class JobSkill(Base):
    __tablename__ = "job_skills"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    is_required = Column(Integer, nullable=False, default=1)
    importance_weight = Column(Float, nullable=False, default=1.0)
    min_years = Column(Float, nullable=False, default=1.0)
    created_at = Column(String(100), default=now_iso)

    __table_args__ = (UniqueConstraint("job_id", "skill_id", name="uq_job_skill"),)

    job = relationship("Job", back_populates="skills")
    skill = relationship("Skill", back_populates="job_skills")
