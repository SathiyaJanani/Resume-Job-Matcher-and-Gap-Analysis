"""
SQLAlchemy ORM models for Applications, Interviews, Learning, Roles, Chat, and Notifications.
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from backend.app.database import Base


def now_iso():
    return datetime.now(timezone.utc).isoformat()


class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    recruiter_id = Column(Integer, ForeignKey("recruiters.id"), nullable=False)
    stage = Column(String(50), nullable=False, default="Applied")  # 'Applied', 'Screening', 'Technical Interview', 'Culture Fit', 'Offer', 'Hired', 'Rejected'
    applied_date = Column(String(100), default=now_iso)
    status = Column(String(50), nullable=False, default="Under Review")
    notes = Column(Text, nullable=True)

    candidate = relationship("Candidate", back_populates="applications")
    job = relationship("Job", back_populates="applications")
    recruiter = relationship("Recruiter", back_populates="applications")
    interviews = relationship("Interview", back_populates="application", cascade="all, delete-orphan")


class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("job_applications.id"), nullable=False)
    recruiter_id = Column(Integer, ForeignKey("recruiters.id"), nullable=False)
    round_name = Column(String(255), nullable=False)
    scheduled_at = Column(String(100), nullable=False)
    duration_minutes = Column(Integer, nullable=False, default=45)
    meeting_link = Column(String(255), nullable=False)
    interviewer_notes = Column(Text, nullable=True)
    rating_score = Column(Float, nullable=True)
    status = Column(String(50), nullable=False, default="Scheduled")
    created_at = Column(String(100), default=now_iso)

    application = relationship("JobApplication", back_populates="interviews")
    recruiter = relationship("Recruiter", back_populates="interviews")


class LearningRecommendation(Base):
    __tablename__ = "learning_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    course_title = Column(String(255), nullable=False)
    platform = Column(String(100), nullable=False)
    url = Column(String(255), nullable=False)
    estimated_hours = Column(Integer, nullable=False, default=20)
    difficulty_level = Column(String(50), nullable=False, default="Intermediate")
    priority = Column(String(50), nullable=False, default="Medium")
    status = Column(String(50), nullable=False, default="Recommended")
    created_at = Column(String(100), default=now_iso)

    candidate = relationship("Candidate", back_populates="learning_recommendations")
    skill = relationship("Skill", back_populates="learning_recommendations")


class RoleProfile(Base):
    __tablename__ = "role_profiles"

    id = Column(Integer, primary_key=True, index=True)
    role_title = Column(String(255), unique=True, index=True, nullable=False)
    category = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    core_skills_json = Column(Text, nullable=False)
    secondary_skills_json = Column(Text, nullable=False)
    average_package = Column(String(100), nullable=False)
    demand_outlook = Column(String(100), nullable=False, default="High Demand")
    created_at = Column(String(100), default=now_iso)


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False, default="Career & NLP Chat")
    created_at = Column(String(100), default=now_iso)
    updated_at = Column(String(100), default=now_iso)

    user = relationship("User", back_populates="chat_sessions")
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False)
    role = Column(String(20), nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    intent_tag = Column(String(100), nullable=True)
    entities_json = Column(Text, nullable=True)
    created_at = Column(String(100), default=now_iso)

    session = relationship("ChatSession", back_populates="messages")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    category = Column(String(100), nullable=False, default="system")
    is_read = Column(Integer, nullable=False, default=0)
    created_at = Column(String(100), default=now_iso)

    user = relationship("User", back_populates="notifications")


class EvaluationBenchmark(Base):
    __tablename__ = "evaluation_benchmarks"

    id = Column(Integer, primary_key=True, index=True)
    pair_name = Column(String(255), nullable=False)
    candidate_name = Column(String(255), nullable=False)
    job_title = Column(String(255), nullable=False)
    ground_truth_relevance = Column(Integer, nullable=False, default=1)  # 1 = relevant, 0 = non-relevant
    keyword_score = Column(Float, nullable=False)
    tfidf_score = Column(Float, nullable=False)
    hybrid_score = Column(Float, nullable=False)
    created_at = Column(String(100), default=now_iso)
