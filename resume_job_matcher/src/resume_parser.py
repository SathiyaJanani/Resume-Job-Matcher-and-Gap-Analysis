"""
resume_parser.py
-----------------
Extracts raw text from a resume file. Supports .pdf, .docx and .txt.
"""

import os


def extract_text_from_pdf(file_path):
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        raise ImportError("PyPDF2 is required to read PDF files. Install with: pip install PyPDF2")

    text = []
    reader = PdfReader(file_path)
    for page in reader.pages:
        page_text = page.extract_text() or ""
        text.append(page_text)
    return "\n".join(text)


def extract_text_from_docx(file_path):
    try:
        import docx
    except ImportError:
        raise ImportError("python-docx is required to read DOCX files. Install with: pip install python-docx")

    document = docx.Document(file_path)
    return "\n".join(p.text for p in document.paragraphs)


def extract_text_from_txt(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def parse_resume(file_path):
    """
    Detects the file extension and routes to the appropriate extractor.
    Returns the raw extracted text (str).
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Resume file not found: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    elif ext == ".txt":
        return extract_text_from_txt(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}. Use .pdf, .docx, or .txt")
