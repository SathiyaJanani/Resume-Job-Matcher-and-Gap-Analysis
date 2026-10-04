"""
skill_extractor.py
-------------------
Extracts a normalized set of skills from a block of text (resume or job
description) by matching against the SKILLS_DATABASE taxonomy.

Uses simple, dependency-light regex/keyword matching so the project runs
without needing to download large NLP models. If spaCy is installed and
available, it is used additionally for noun-phrase based discovery of
skills that are NOT already in the taxonomy ("possible additional skills").
"""

import re
from src.skills_database import SKILLS_DATABASE


def _normalize(text):
    return text.lower()


def extract_known_skills(text):
    """
    Returns a sorted list of canonical skill names found in `text`,
    matched against SKILLS_DATABASE aliases.
    """
    text_norm = _normalize(text)
    found = set()

    for canonical_skill, aliases in SKILLS_DATABASE.items():
        for alias in aliases:
            pattern = r"(?<![a-zA-Z0-9])" + re.escape(alias.strip()) + r"(?![a-zA-Z0-9])"
            if re.search(pattern, text_norm):
                found.add(canonical_skill)
                break

    return sorted(found)


def extract_additional_candidate_skills(text, known_skills):
    """
    Best-effort discovery of extra skill-like tokens not covered by the
    taxonomy, using spaCy noun chunks if spaCy + a model are available.
    Falls back to an empty list if spaCy isn't installed. This is
    supplementary and not required for core matching.
    """
    try:
        import spacy
        try:
            nlp = spacy.load("en_core_web_sm")
        except OSError:
            return []
    except ImportError:
        return []

    doc = nlp(text[:100000])  # guard against very large inputs
    candidates = set()
    stop_like = {"experience", "years", "team", "company", "role", "candidate"}

    for chunk in doc.noun_chunks:
        phrase = chunk.text.strip().lower()
        if (
            2 <= len(phrase) <= 30
            and phrase not in known_skills
            and phrase not in stop_like
            and not phrase.isdigit()
        ):
            candidates.add(phrase)

    return sorted(candidates)[:15]  # cap noise
