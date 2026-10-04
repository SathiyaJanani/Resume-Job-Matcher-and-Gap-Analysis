"""
text_extractor.py
------------------
Utility functions to pull raw text out of resumes / job description files.
Supports .txt, .pdf and .docx. Falls back gracefully if optional
dependencies (PyPDF2, python-docx) are not installed.
"""

import os


def extract_text(file_path: str) -> str:
    """Return the raw text content of a resume/job-description file."""
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".txt":
        return _extract_txt(file_path)
    elif ext == ".pdf":
        return _extract_pdf(file_path)
    elif ext in (".docx", ".doc"):
        return _extract_docx(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")


def _extract_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def _extract_pdf(file_path: str) -> str:
    try:
        from PyPDF2 import PdfReader
    except ImportError as exc:
        raise ImportError(
            "PyPDF2 is required to read PDF files. Install it with "
            "'pip install PyPDF2'."
        ) from exc

    reader = PdfReader(file_path)
    text = []
    for page in reader.pages:
        text.append(page.extract_text() or "")
    return "\n".join(text)


def _extract_docx(file_path: str) -> str:
    try:
        import docx
    except ImportError as exc:
        raise ImportError(
            "python-docx is required to read DOCX files. Install it with "
            "'pip install python-docx'."
        ) from exc

    document = docx.Document(file_path)
    return "\n".join(p.text for p in document.paragraphs)
