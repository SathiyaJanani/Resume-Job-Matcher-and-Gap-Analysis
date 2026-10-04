"""
Enterprise Database Schema and Connection Management for Resume Intelligence Platform.
Contains definitions for all 12 core tables.
"""

import os
import sqlite3
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent
DB_PATH = BACKEND_DIR / "recruitment_hub.db"


def get_db_path() -> Path:
    return DB_PATH


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db(force: bool = False):
    """Initialize all 12 tables in the database."""
    if force and DB_PATH.exists():
        try:
            DB_PATH.unlink()
        except Exception:
            pass

    with get_connection() as conn:
        cursor = conn.cursor()

        # 1. Candidates table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL,
            location TEXT NOT NULL,
            current_title TEXT NOT NULL,
            years_experience REAL NOT NULL,
            highest_degree TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Active',
            created_at TEXT NOT NULL
        );
        """)

        # 2. Companies table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            industry TEXT NOT NULL,
            size_range TEXT NOT NULL,
            headquarters TEXT NOT NULL,
            website TEXT NOT NULL,
            rating REAL NOT NULL,
            verified INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL
        );
        """)

        # 3. Recruiters table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS recruiters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            role TEXT NOT NULL,
            department TEXT NOT NULL,
            active_requisitions INTEGER NOT NULL DEFAULT 0,
            phone TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (company_id) REFERENCES companies (id) ON DELETE CASCADE
        );
        """)

        # 4. Jobs table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            recruiter_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            department TEXT NOT NULL,
            employment_type TEXT NOT NULL,
            experience_level TEXT NOT NULL,
            location_type TEXT NOT NULL,
            salary_range TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Open',
            created_at TEXT NOT NULL,
            FOREIGN KEY (company_id) REFERENCES companies (id) ON DELETE CASCADE,
            FOREIGN KEY (recruiter_id) REFERENCES recruiters (id) ON DELETE CASCADE
        );
        """)

        # 5. Skills table (Taxonomy)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            skill_name TEXT NOT NULL UNIQUE,
            category TEXT NOT NULL,
            demand_score INTEGER NOT NULL,
            popularity_level TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        """)

        # 6. Candidate Skills table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS candidate_skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id INTEGER NOT NULL,
            skill_id INTEGER NOT NULL,
            proficiency_level TEXT NOT NULL,
            years_experience REAL NOT NULL,
            verified INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL,
            FOREIGN KEY (candidate_id) REFERENCES candidates (id) ON DELETE CASCADE,
            FOREIGN KEY (skill_id) REFERENCES skills (id) ON DELETE CASCADE,
            UNIQUE(candidate_id, skill_id)
        );
        """)

        # 7. Job Skills table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER NOT NULL,
            skill_id INTEGER NOT NULL,
            is_required INTEGER NOT NULL DEFAULT 1,
            importance_weight REAL NOT NULL DEFAULT 1.0,
            min_years REAL NOT NULL DEFAULT 1.0,
            created_at TEXT NOT NULL,
            FOREIGN KEY (job_id) REFERENCES jobs (id) ON DELETE CASCADE,
            FOREIGN KEY (skill_id) REFERENCES skills (id) ON DELETE CASCADE,
            UNIQUE(job_id, skill_id)
        );
        """)

        # 8. Resumes table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id INTEGER NOT NULL,
            file_name TEXT NOT NULL,
            file_size_kb INTEGER NOT NULL,
            raw_text TEXT NOT NULL,
            parsed_summary TEXT NOT NULL,
            ai_detected_seniority TEXT NOT NULL,
            uploaded_at TEXT NOT NULL,
            FOREIGN KEY (candidate_id) REFERENCES candidates (id) ON DELETE CASCADE
        );
        """)

        # 9. Job Applications table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id INTEGER NOT NULL,
            job_id INTEGER NOT NULL,
            recruiter_id INTEGER NOT NULL,
            stage TEXT NOT NULL DEFAULT 'Applied',
            applied_date TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Under Review',
            notes TEXT,
            FOREIGN KEY (candidate_id) REFERENCES candidates (id) ON DELETE CASCADE,
            FOREIGN KEY (job_id) REFERENCES jobs (id) ON DELETE CASCADE,
            FOREIGN KEY (recruiter_id) REFERENCES recruiters (id) ON DELETE CASCADE
        );
        """)

        # 10. Match Results table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS match_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id INTEGER NOT NULL,
            job_id INTEGER NOT NULL,
            match_score REAL NOT NULL,
            semantic_similarity REAL NOT NULL,
            skill_overlap_score REAL NOT NULL,
            readiness_percentage REAL NOT NULL,
            matched_skills TEXT NOT NULL,
            missing_skills TEXT NOT NULL,
            ai_summary TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (candidate_id) REFERENCES candidates (id) ON DELETE CASCADE,
            FOREIGN KEY (job_id) REFERENCES jobs (id) ON DELETE CASCADE
        );
        """)

        # 11. Interviews table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS interviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            application_id INTEGER NOT NULL,
            recruiter_id INTEGER NOT NULL,
            round_name TEXT NOT NULL,
            scheduled_at TEXT NOT NULL,
            duration_minutes INTEGER NOT NULL,
            meeting_link TEXT NOT NULL,
            interviewer_notes TEXT,
            rating_score REAL,
            status TEXT NOT NULL DEFAULT 'Scheduled',
            created_at TEXT NOT NULL,
            FOREIGN KEY (application_id) REFERENCES job_applications (id) ON DELETE CASCADE,
            FOREIGN KEY (recruiter_id) REFERENCES recruiters (id) ON DELETE CASCADE
        );
        """)

        # 12. Learning Recommendations table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS learning_recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id INTEGER NOT NULL,
            skill_id INTEGER NOT NULL,
            course_title TEXT NOT NULL,
            platform TEXT NOT NULL,
            url TEXT NOT NULL,
            estimated_hours INTEGER NOT NULL,
            difficulty_level TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Recommended',
            created_at TEXT NOT NULL,
            FOREIGN KEY (candidate_id) REFERENCES candidates (id) ON DELETE CASCADE,
            FOREIGN KEY (skill_id) REFERENCES skills (id) ON DELETE CASCADE
        );
        """)

        conn.commit()


TABLE_NAMES = [
    "candidates",
    "companies",
    "recruiters",
    "jobs",
    "skills",
    "candidate_skills",
    "job_skills",
    "resumes",
    "job_applications",
    "match_results",
    "interviews",
    "learning_recommendations",
]


def get_table_counts() -> dict[str, int]:
    """Return record counts for all 12 tables."""
    counts = {}
    with get_connection() as conn:
        cursor = conn.cursor()
        for tbl in TABLE_NAMES:
            cursor.execute(f"SELECT COUNT(*) FROM {tbl}")
            counts[tbl] = cursor.fetchone()[0]
    return counts
