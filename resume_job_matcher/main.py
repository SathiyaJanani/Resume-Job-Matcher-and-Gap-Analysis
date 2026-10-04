"""
main.py
-------
AI Based Intelligent Resume-Job Matching & Skill Gap Analysis
CLI entry point.

Usage:
    python main.py --resume sample_data/sample_resume.txt --job sample_data/sample_job_description.txt

    # Or with PDF / DOCX resumes:
    python main.py --resume path/to/resume.pdf --job path/to/job_description.txt
"""

import argparse
import sys

from src.resume_parser import parse_resume
from src.job_parser import load_job_description
from src.skill_extractor import extract_known_skills, extract_additional_candidate_skills
from src.matcher import compute_match_score
from src.skill_gap_analyzer import analyze_skill_gap
from src.report_generator import print_console_report, save_json_report


def run(resume_path, job_source, save_report=True):
    print("Reading resume...")
    resume_text = parse_resume(resume_path)

    print("Reading job description...")
    job_text = load_job_description(job_source)

    print("Extracting skills...")
    resume_skills = extract_known_skills(resume_text)
    job_skills = extract_known_skills(job_text)

    extra_candidates = extract_additional_candidate_skills(resume_text, resume_skills)

    print("Computing match score...")
    match_result = compute_match_score(resume_text, job_text, resume_skills, job_skills)

    print("Running skill gap analysis...")
    gap_result = analyze_skill_gap(resume_skills, job_skills)

    print_console_report(match_result, gap_result, resume_skills, job_skills)

    if extra_candidates:
        print("\n(Info) Other potential skill-like phrases detected in the resume")
        print("       that aren't in the built-in taxonomy (review manually):")
        print("  " + ", ".join(extra_candidates))

    if save_report:
        path = save_json_report(match_result, gap_result, resume_skills, job_skills)
        print(f"\nJSON report saved to: {path}")

    return match_result, gap_result


def main():
    parser = argparse.ArgumentParser(
        description="AI Based Intelligent Resume-Job Matching & Skill Gap Analysis"
    )
    parser.add_argument("--resume", required=True, help="Path to resume file (.pdf, .docx, .txt)")
    parser.add_argument("--job", required=True, help="Path to job description .txt file, or raw text")
    parser.add_argument("--no-save", action="store_true", help="Don't save a JSON report to disk")

    args = parser.parse_args()

    try:
        run(args.resume, args.job, save_report=not args.no_save)
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
