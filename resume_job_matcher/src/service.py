"""Application service shared by Streamlit, CLI integrations, and FastAPI."""

from src.advanced_nlp import extract_dynamic_phrases, extract_profile, explain_matches, semantic_similarity
from src.learned_matcher import feature_vector, predict_fit
from src.skill_extractor import extract_known_skills
from src.skill_gap_analyzer import analyze_skill_gap


def analyze_pair(resume_text: str, job_text: str) -> dict:
    resume_skills = extract_known_skills(resume_text)
    job_skills = extract_known_skills(job_text)
    gap = analyze_skill_gap(resume_skills, job_skills)
    semantic = semantic_similarity(resume_text, job_text)
    skill_overlap = len(set(resume_skills) & set(job_skills)) / len(job_skills) if job_skills else 0.0
    phrases = extract_dynamic_phrases(job_text)
    evidence = sum(phrase.lower() in resume_text.lower() for phrase in phrases) / len(phrases) if phrases else skill_overlap
    resume_profile = extract_profile(resume_text)
    job_profile = extract_profile(job_text)
    required_years = job_profile["total_years_experience"]
    experience = min(resume_profile["total_years_experience"] / required_years, 1.0) if required_years else 0.75
    score = predict_fit(feature_vector(semantic, semantic, skill_overlap, experience, evidence))
    return {
        "final_match_score": score,
        "semantic_similarity_score": round(semantic * 100, 2),
        "skill_overlap_score": round(skill_overlap * 100, 2),
        "dynamic_phrases": phrases,
        "matched_skills": sorted(set(resume_skills) & set(job_skills)),
        "missing_skills": sorted(set(job_skills) - set(resume_skills)),
        "extra_skills": gap["extra_skills"],
        "readiness_percentage": gap["readiness_percentage"],
        "learning_suggestions": gap["learning_suggestions"],
        "learning_plan": gap["learning_plan"],
        "profile": resume_profile,
        "job_profile": job_profile,
        "evidence": explain_matches(resume_text, job_text, phrases),
    }


def rank_resumes(resumes: list[dict[str, str]], job_text: str) -> list[dict]:
    ranked = [{"name": resume["name"], "result": analyze_pair(resume["text"], job_text)} for resume in resumes]
    return sorted(ranked, key=lambda item: item["result"]["final_match_score"], reverse=True)