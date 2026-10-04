"""Semantic embeddings, NER-backed profile extraction, and dynamic phrases."""

import re
from functools import lru_cache
from typing import Any

import numpy as np


@lru_cache(maxsize=1)
def _embedding_model():
    try:
        from sentence_transformers import SentenceTransformer
        return SentenceTransformer("all-MiniLM-L6-v2")
    except (ImportError, OSError, RuntimeError):
        return None


def semantic_similarity(left: str, right: str) -> float:
    """Return cosine similarity in [0, 1], using embeddings with a local fallback."""
    model = _embedding_model()
    if model is not None:
        vectors = model.encode([left, right], normalize_embeddings=True)
        return float(np.dot(vectors[0], vectors[1]))

    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    matrix = TfidfVectorizer(stop_words="english").fit_transform([left, right])
    return float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0])


def _spacy_doc(text: str) -> Any:
    try:
        import spacy
        try:
            return spacy.load("en_core_web_sm")(text[:100000])
        except OSError:
            return None
    except ImportError:
        return None


def extract_profile(text: str) -> dict[str, Any]:
    """Extract structured candidate/job facts, degrading cleanly without a model."""
    doc = _spacy_doc(text)
    entities = [{"text": ent.text.strip(), "label": ent.label_} for ent in doc.ents] if doc else []
    names = [item["text"] for item in entities if item["label"] == "PERSON"]
    organizations = [item["text"] for item in entities if item["label"] in {"ORG", "GPE"}]
    education = _section(text, "education|academic|qualification")
    certifications = _section(text, "certification|certified")
    projects = _section(text, "projects?|portfolio")
    years = [float(value) for value in re.findall(r"(?<!\d)(\d+(?:\.\d+)?)\+?\s+years?", text.lower())]

    if not names:
        first_line = next((line.strip() for line in text.splitlines() if line.strip()), "")
        if 1 < len(first_line.split()) <= 5 and not any(char.isdigit() for char in first_line):
            names = [first_line]

    return {
        "candidate_name": names[0] if names else None,
        "education": education,
        "total_years_experience": max(years, default=0.0),
        "certifications": certifications,
        "projects": projects,
        "entities": entities,
        "organizations": organizations,
    }


def _section(text: str, headings: str) -> list[str]:
    pattern = rf"(?:^|\n)\s*(?:{headings})\s*:?(.*?)(?=\n\s*[A-Z][A-Za-z &/-]{{2,30}}\s*:?(?:\n|$)|\Z)"
    matches = re.findall(pattern, text, flags=re.IGNORECASE | re.DOTALL)
    return [re.sub(r"\s+", " ", match).strip()[:500] for match in matches if match.strip()]


def extract_dynamic_phrases(text: str, limit: int = 25) -> list[str]:
    """Discover phrases outside the fixed taxonomy using KeyBERT or noun chunks."""
    try:
        from keybert import KeyBERT
        model = _embedding_model()
        keywords = KeyBERT(model=model).extract_keywords(text[:20000], keyphrase_ngram_range=(1, 3), stop_words="english", top_n=limit)
        return [phrase for phrase, _ in keywords]
    except (ImportError, OSError, RuntimeError, ValueError):
        doc = _spacy_doc(text)
        if not doc:
            return []
        phrases = {chunk.text.lower().strip() for chunk in doc.noun_chunks if 2 <= len(chunk.text.strip()) <= 60}
        return sorted(phrases, key=lambda value: (-len(value.split()), value))[:limit]


def explain_matches(resume_text: str, job_text: str, phrases: list[str]) -> list[dict[str, str]]:
    """Return resume snippets containing discovered evidence for the explanation panel."""
    explanations = []
    lowered = resume_text.lower()
    for phrase in phrases:
        position = lowered.find(phrase.lower())
        if position >= 0:
            start = max(0, position - 90)
            end = min(len(resume_text), position + len(phrase) + 120)
            explanations.append({"phrase": phrase, "evidence": resume_text[start:end].replace("\n", " ")})
    return explanations[:15]