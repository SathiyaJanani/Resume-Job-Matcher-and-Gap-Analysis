"""
Models package initialization.
Exports all SQLAlchemy models for Base.metadata discovery.
"""

from backend.app.database import Base
from backend.app.models.user import User, Candidate, Recruiter
from backend.app.models.opportunity import Company, Job
from backend.app.models.skill import Skill, SkillAlias, CandidateSkill, JobSkill
from backend.app.models.matching import Resume, MatchResult, SkillGapReport
from backend.app.models.application import (
    JobApplication,
    Interview,
    LearningRecommendation,
    RoleProfile,
    ChatSession,
    ChatMessage,
    Notification,
    EvaluationBenchmark,
)

__all__ = [
    "Base",
    "User",
    "Candidate",
    "Recruiter",
    "Company",
    "Job",
    "Skill",
    "SkillAlias",
    "CandidateSkill",
    "JobSkill",
    "Resume",
    "MatchResult",
    "SkillGapReport",
    "JobApplication",
    "Interview",
    "LearningRecommendation",
    "RoleProfile",
    "ChatSession",
    "ChatMessage",
    "Notification",
    "EvaluationBenchmark",
]
