# Resume Intelligence Platform

An advanced resume intelligence platform with semantic matching, structured
candidate extraction, learned fit scoring, recruiter ranking, explainability,
and an API-backed workflow.

## Capabilities

- PDF, DOCX, and TXT resume parsing
- `all-MiniLM-L6-v2` sentence embeddings with TF-IDF fallback
- spaCy NER for names, organizations, education, certifications, projects,
  and experience years
- KeyBERT or spaCy noun-chunk phrase discovery beyond the legacy taxonomy
- Random Forest fit scorer bootstrapped on synthetic labeled data
- Recruiter batch ranking for many resumes against one job
- Evidence snippets showing why a score was given
- SQLite locally, with `DATABASE_URL` support for PostgreSQL deployments
- FastAPI REST endpoints and a Streamlit recruiter interface

## Setup

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## Run

```bash
streamlit run app.py
uvicorn api:app --reload
```

The API exposes `GET /health`, `POST /matches`, `GET /matches`, and
`POST /resumes/parse`. The included `Dockerfile` and `render.yaml` provide a
deployment starting point for Render, Hugging Face Spaces, or another
container host. Set `DATABASE_URL` to managed PostgreSQL in production.

## Architecture

- `src/advanced_nlp.py`: embeddings, NER, dynamic phrase extraction, evidence
- `src/learned_matcher.py`: reproducible bootstrap training and inference
- `src/service.py`: shared single-match and batch-ranking business logic
- `src/database.py`: persisted resumes, jobs, and match history
- `api.py`: REST API
- `app.py`: recruiter-facing Streamlit UI

The initial model is explicitly labeled as synthetic bootstrap data. Replace
it with recruiter outcomes and validate offline before production use. The
model features are semantic similarity, legacy text similarity, skill
coverage, experience alignment, and evidence coverage.

## Legacy CLI

```bash
python main.py --resume sample_data/sample_resume.txt --job sample_data/sample_job_description.txt
```