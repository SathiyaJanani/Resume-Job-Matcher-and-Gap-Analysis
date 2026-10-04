"""
report_generator.py
--------------------
Formats the results of matching + skill gap analysis into:
1. A human-readable console report.
2. A JSON report saved to disk.
"""

import json
import os
from datetime import datetime


def print_console_report(match_result, gap_result, resume_skills, job_skills):
    line = "=" * 60
    print(line)
    print("RESUME - JOB MATCH REPORT")
    print(line)

    print(f"\nOverall Match Score : {match_result['final_match_score']}%")
    print(f"  - Text Similarity  : {match_result['text_similarity_score']}%")
    print(f"  - Skill Overlap    : {match_result['skill_overlap_score']}%")

    print(f"\nSkill Readiness      : {gap_result['readiness_percentage']}%")

    print(f"\nResume Skills Detected ({len(resume_skills)}):")
    print("  " + (", ".join(resume_skills) if resume_skills else "None detected"))

    print(f"\nJob Required Skills ({len(job_skills)}):")
    print("  " + (", ".join(job_skills) if job_skills else "None detected"))

    print(f"\n✔ Matched Skills ({len(gap_result['matched_skills'])}):")
    print("  " + (", ".join(gap_result["matched_skills"]) if gap_result["matched_skills"] else "None"))

    print(f"\n✘ Missing Skills ({len(gap_result['missing_skills'])}):")
    print("  " + (", ".join(gap_result["missing_skills"]) if gap_result["missing_skills"] else "None"))

    if gap_result["missing_skills"]:
        print("\nSuggested Learning Resources for Missing Skills:")
        for skill in gap_result["missing_skills"]:
            resource = gap_result["learning_suggestions"].get(skill, "")
            print(f"  - {skill}: {resource}")

    print(f"\n+ Extra Skills (not required by this job) ({len(gap_result['extra_skills'])}):")
    print("  " + (", ".join(gap_result["extra_skills"]) if gap_result["extra_skills"] else "None"))

    print("\n" + line)


def save_json_report(match_result, gap_result, resume_skills, job_skills, output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(output_dir, f"match_report_{timestamp}.json")

    report = {
        "generated_at": datetime.now().isoformat(),
        "match_result": match_result,
        "skill_gap_analysis": gap_result,
        "resume_skills_detected": resume_skills,
        "job_skills_detected": job_skills,
    }

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    return file_path
