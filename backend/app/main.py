"""
SkillBridge AI - Main FastAPI Application.
Exposes modular routers for Auth, Opportunities, Skills, Resumes, Matcher, Gap Analyzer, and Chatbot.
"""

from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from backend.app.config import settings
from backend.app.routers import auth

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Enterprise NLP-driven Resume Matching & Skill Gap Analysis Platform"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount core routers
app.include_router(auth.router, prefix=settings.API_V1_STR)

FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


@app.get("/api/health")
def health():
    return {
        "status": "healthy",
        "product": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "database": "SQLite (recruitment_hub.db)",
    }


@app.get("/")
def serve_index():
    index_path = FRONTEND_DIR / "index.html"
    if index_path.exists():
        return HTMLResponse(content=index_path.read_text(encoding="utf-8"))
    return HTMLResponse(content=f"<h1>{settings.PROJECT_NAME} Backend Online</h1><p>Visit /docs for OpenAPI docs</p>")
