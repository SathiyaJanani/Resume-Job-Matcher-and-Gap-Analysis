"""Recruiter-facing Streamlit client for the Resume Intelligence platform."""

import os
import tempfile

import streamlit as st

from src.database import init_db, recent_matches, save_match
from src.resume_parser import parse_resume
from src.service import analyze_pair, rank_resumes

st.set_page_config(page_title="Resume Intelligence", page_icon="RI", layout="wide")
init_db()


def read_upload(uploaded_file) -> str:
    suffix = os.path.splitext(uploaded_file.name)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp:
        temp.write(uploaded_file.getvalue())
        path = temp.name
    try:
        return parse_resume(path)
    finally:
        os.remove(path)


def render_result(result: dict, title: str = "Match intelligence"):
    st.subheader(title)
    score, semantic, skills = st.columns(3)
    score.metric("Learned fit score", f"{result['final_match_score']}%")
    semantic.metric("Semantic similarity", f"{result['semantic_similarity_score']}%")
    skills.metric("Required skills covered", f"{result['skill_overlap_score']}%")

    profile = result.get("profile", {})
    st.write("**Candidate profile**")
    st.json({key: value for key, value in profile.items() if key not in {"entities", "organizations"}}, expanded=False)

    matched, missing = st.columns(2)
    matched.success("Matched skills\n\n" + (", ".join(result["matched_skills"]) or "None detected"))
    missing.warning("Missing skills\n\n" + (", ".join(result["missing_skills"]) or "None detected"))

    st.subheader("Skill gap and improvement plan")
    readiness, extras = st.columns(2)
    readiness.metric("Job readiness", f"{result['readiness_percentage']}%")
    extras.info("Additional strengths\n\n" + (", ".join(result["extra_skills"]) or "None detected"))
    st.progress(result["readiness_percentage"] / 100)
    if result["learning_plan"]:
        for item in result["learning_plan"]:
            with st.expander(f"{item['priority'].title()} priority: {item['skill']}"):
                st.write(item["reason"])
                st.write(f"**Practice action:** {item['practice_action']}")
                st.link_button("Open learning resource", item["resource"], use_container_width=False)
    else:
        st.success("No missing taxonomy skills detected. Focus on stronger evidence and measurable outcomes in the resume.")

    st.write("**Evidence found in resume**")
    if result["evidence"]:
        for item in result["evidence"]:
            st.markdown(f"- **{item['phrase']}**: ...{item['evidence']}...")
    else:
        st.info("No exact evidence phrase was found. Semantic similarity may still capture equivalent meaning.")

    with st.expander("Discovered job phrases"):
        st.write(", ".join(result["dynamic_phrases"]) or "No dynamic phrases available")


st.title("Resume Intelligence")
st.caption("Semantic matching, structured extraction, learned scoring, and recruiter ranking")

single_tab, batch_tab, history_tab = st.tabs(["Single match", "Recruiter batch", "Match history"])

with single_tab:
    uploaded_resume = st.file_uploader("Resume", type=["pdf", "docx", "txt"], key="single_resume")
    job_text = st.text_area("Job description", height=220, key="single_job")
    if st.button("Analyze match", type="primary"):
        if not uploaded_resume or not job_text.strip():
            st.error("Upload a resume and provide a job description.")
        else:
            resume_text = read_upload(uploaded_resume)
            result = analyze_pair(resume_text, job_text)
            save_match(uploaded_resume.name, resume_text, "Streamlit job", job_text, result)
            render_result(result)

with batch_tab:
    uploaded_resumes = st.file_uploader("Resumes to rank", type=["pdf", "docx", "txt"], accept_multiple_files=True, key="batch_resumes")
    batch_job = st.text_area("Target job description", height=220, key="batch_job")
    if st.button("Rank candidates", type="primary"):
        if not uploaded_resumes or not batch_job.strip():
            st.error("Upload at least one resume and provide a target job description.")
        else:
            records = [{"name": item.name, "text": read_upload(item)} for item in uploaded_resumes]
            ranking = rank_resumes(records, batch_job)
            st.subheader("Candidate leaderboard")
            for index, candidate in enumerate(ranking, start=1):
                result = candidate["result"]
                with st.container(border=True):
                    left, right = st.columns([4, 1])
                    left.write(f"**#{index}  {candidate['name']}**")
                    right.metric("Fit", f"{result['final_match_score']}%")
                    st.progress(result["final_match_score"] / 100)
                    st.caption("Matched: " + (", ".join(result["matched_skills"]) or "No taxonomy skills detected"))
                    with st.expander("Why this rank?"):
                        render_result(result, candidate["name"])

with history_tab:
    st.subheader("Persisted match history")
    history = recent_matches()
    if history:
        st.dataframe([{"id": item["id"], "score": item["score"], "created_at": item["created_at"]} for item in history], use_container_width=True)
    else:
        st.info("No matches have been saved yet.")