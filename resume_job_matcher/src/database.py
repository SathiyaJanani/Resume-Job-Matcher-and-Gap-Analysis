"""SQLite persistence layer; set DATABASE_URL to a PostgreSQL URL in production."""

import json
import os
import sqlite3
from datetime import datetime, timezone

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///resume_matcher.db")
DB_PATH = DATABASE_URL.removeprefix("sqlite:///") if DATABASE_URL.startswith("sqlite") else "resume_matcher.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_connection() as connection:
        connection.executescript("""
        CREATE TABLE IF NOT EXISTS resumes (id INTEGER PRIMARY KEY, name TEXT NOT NULL, content TEXT NOT NULL, profile_json TEXT, created_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS jobs (id INTEGER PRIMARY KEY, title TEXT NOT NULL, content TEXT NOT NULL, created_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS matches (id INTEGER PRIMARY KEY, resume_id INTEGER NOT NULL, job_id INTEGER NOT NULL, score REAL NOT NULL, result_json TEXT NOT NULL, created_at TEXT NOT NULL);
        """)


def save_match(resume_name: str, resume_text: str, job_title: str, job_text: str, result: dict) -> int:
    now = datetime.now(timezone.utc).isoformat()
    with get_connection() as connection:
        resume = connection.execute("INSERT INTO resumes(name, content, profile_json, created_at) VALUES (?, ?, ?, ?)", (resume_name, resume_text, json.dumps(result.get("profile", {})), now))
        job = connection.execute("INSERT INTO jobs(title, content, created_at) VALUES (?, ?, ?)", (job_title, job_text, now))
        match = connection.execute("INSERT INTO matches(resume_id, job_id, score, result_json, created_at) VALUES (?, ?, ?, ?, ?)", (resume.lastrowid, job.lastrowid, result["final_match_score"], json.dumps(result), now))
        return int(match.lastrowid)


def recent_matches(limit: int = 50) -> list[dict]:
    with get_connection() as connection:
        rows = connection.execute("SELECT id, score, created_at, result_json FROM matches ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    return [{"id": row["id"], "score": row["score"], "created_at": row["created_at"], **json.loads(row["result_json"])} for row in rows]