"""
matcher.py
----------
Computes an overall match score between a resume and a job description
using two complementary signals:

1. TF-IDF cosine similarity over the full text (captures overall
   contextual/semantic overlap of wording).
2. Skill-set overlap (captures how many of the job's required skills
   are actually present in the resume).

The final score is a weighted blend of the two.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.advanced_nlp import semantic_similarity
from src.learned_matcher import feature_vector, predict_fit


def compute_text_similarity(resume_text, job_text):
    """Returns a 0-100 similarity score based on TF-IDF cosine similarity."""
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform([resume_text, job_text])
    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return round(score * 100, 2)


def compute_skill_overlap(resume_skills, job_skills):
    """Returns a 0-100 score based on the fraction of job skills present in the resume."""
    if not job_skills:
        return 0.0
    matched = set(resume_skills) & set(job_skills)
    return round((len(matched) / len(job_skills)) * 100, 2)


def compute_match_score(resume_text, job_text, resume_skills, job_skills,
                         text_weight=0.4, skill_weight=0.6):
    """
    Combines text similarity and skill overlap into one final score.
    Skill overlap is weighted higher by default since it's the more
    direct/interpretable signal for resume-job fit.
    """
    text_score = compute_text_similarity(resume_text, job_text)
    semantic_score = round(semantic_similarity(resume_text, job_text) * 100, 2)
    skill_score = compute_skill_overlap(resume_skills, job_skills)
    final_score = predict_fit(feature_vector(semantic_score / 100, text_score / 100, skill_score / 100, 0.75, skill_score / 100))

    return {
        "final_match_score": final_score,
        "text_similarity_score": text_score,
        "semantic_similarity_score": semantic_score,
        "skill_overlap_score": skill_score,
    }
