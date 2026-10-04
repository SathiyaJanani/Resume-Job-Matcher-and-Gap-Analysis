"""
skill_gap_analyzer.py
----------------------
Compares the resume's skill set against the job's required skill set and
produces a structured gap analysis: matched skills, missing skills, and
extra skills the candidate has beyond what the job asks for.
"""

import json
from pathlib import Path

# Kept as a fallback for installations that do not include the data file.
LEARNING_SUGGESTIONS = {
    "python": "Official docs: docs.python.org/3/tutorial",
    "machine learning": "Andrew Ng's Machine Learning course (Coursera)",
    "deep learning": "deeplearning.ai specialization (Coursera)",
    "natural language processing": "Hugging Face NLP course (huggingface.co/course)",
    "sql": "Mode SQL Tutorial (mode.com/sql-tutorial)",
    "react": "react.dev official docs",
    "aws": "AWS Cloud Practitioner Essentials (AWS Skill Builder)",
    "docker": "Docker official 'Get Started' guide (docs.docker.com)",
    "git": "git-scm.com/book (Pro Git)",
    "data structures": "GeeksforGeeks DSA self-paced course",
}

RESOURCE_PATH = Path(__file__).resolve().parent.parent / "data" / "learning_resources.json"


def _load_learning_resources():
    try:
        with RESOURCE_PATH.open(encoding="utf-8") as source:
            return {**LEARNING_SUGGESTIONS, **json.load(source)}
    except (OSError, json.JSONDecodeError):
        return LEARNING_SUGGESTIONS


def analyze_skill_gap(resume_skills, job_skills):
    resume_set = set(resume_skills)
    job_set = set(job_skills)

    matched = sorted(resume_set & job_set)
    missing = sorted(job_set - resume_set)
    extra = sorted(resume_set - job_set)

    if job_set:
        readiness_pct = round((len(matched) / len(job_set)) * 100, 2)
    else:
        readiness_pct = 0.0

    resources = _load_learning_resources()
    suggestions = {
        skill: resources.get(skill, resources.get("default", "Search for a well-reviewed course or official documentation."))
        for skill in missing
    }
    learning_plan = [
        {
            "skill": skill,
            "priority": "high" if index < max(1, len(missing) // 2) else "medium",
            "reason": "Required by the target job and not detected in the resume.",
            "resource": suggestions[skill],
            "practice_action": f"Build one small portfolio project that demonstrates {skill} and add measurable results to your resume.",
        }
        for index, skill in enumerate(missing)
    ]

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "extra_skills": extra,
        "readiness_percentage": readiness_pct,
        "learning_suggestions": suggestions,
        "learning_plan": learning_plan,
    }
