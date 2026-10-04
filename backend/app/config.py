"""
Configuration module for SkillBridge AI Platform.
Loads environment variables and sets defaults for security, database, and scoring weights.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "backend" / "recruitment_hub.db"


class Settings:
    PROJECT_NAME: str = "SkillBridge AI"
    VERSION: str = "2.0.0"
    API_V1_STR: str = "/api"

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "skillbridge_super_secret_jwt_key_2026_academic_demo")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days for demo ease

    # Database (preserves existing SQLite database file)
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{DB_PATH}")

    # NLP Matching Weights (Sum to 1.0)
    WEIGHT_SKILL_OVERLAP: float = float(os.getenv("WEIGHT_SKILL_OVERLAP", "0.40"))
    WEIGHT_TFIDF: float = float(os.getenv("WEIGHT_TFIDF", "0.20"))
    WEIGHT_SEMANTIC: float = float(os.getenv("WEIGHT_SEMANTIC", "0.20"))
    WEIGHT_EXPERIENCE: float = float(os.getenv("WEIGHT_EXPERIENCE", "0.10"))
    WEIGHT_ELIGIBILITY: float = float(os.getenv("WEIGHT_ELIGIBILITY", "0.10"))

    # ATS Weights
    ATS_SECTION_WEIGHT: float = 0.25
    ATS_KEYWORD_WEIGHT: float = 0.35
    ATS_ACTION_VERBS_WEIGHT: float = 0.20
    ATS_QUANTIFIED_WEIGHT: float = 0.20


settings = Settings()
