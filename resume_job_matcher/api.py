"""REST API for resume ingestion, matching, ranking, and match history."""

from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel
from src.database import init_db, recent_matches, save_match
from src.resume_parser import parse_resume
from src.service import analyze_pair
import os
import tempfile

app = FastAPI(title="Resume Intelligence API", version="1.0.0")
init_db()


class MatchRequest(BaseModel):
    resume_text: str
    job_text: str
    resume_name: str = "api-resume"
    job_title: str = "api-job"


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/matches")
def match(request: MatchRequest):
    result = analyze_pair(request.resume_text, request.job_text)
    result["match_id"] = save_match(request.resume_name, request.resume_text, request.job_title, request.job_text, result)
    return result


@app.get("/matches")
def history(limit: int = 50):
    return recent_matches(max(1, min(limit, 200)))


@app.post("/resumes/parse")
async def parse_uploaded_resume(file: UploadFile = File(...)):
    suffix = os.path.splitext(file.filename or "resume.txt")[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp:
        temp.write(await file.read())
        path = temp.name
    try:
        return {"filename": file.filename, "text": parse_resume(path)}
    except (ValueError, FileNotFoundError) as error:
        raise HTTPException(status_code=400, detail=str(error))
    finally:
        os.remove(path)