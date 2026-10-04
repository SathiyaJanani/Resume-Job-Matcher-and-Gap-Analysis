"""
job_parser.py
-------------
Loads and lightly cleans a job description (from a .txt file or raw string).
"""

import os
import re


def load_job_description(source):
    """
    Accepts either a file path to a .txt file or a raw string of the
    job description text, and returns cleaned text.
    """
    if os.path.exists(source) and source.lower().endswith(".txt"):
        with open(source, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
    else:
        text = source

    return clean_text(text)


def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()
