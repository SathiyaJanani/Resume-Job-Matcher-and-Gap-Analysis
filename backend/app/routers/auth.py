"""
Authentication Router for SkillBridge AI.
Handles User Registration, Login (JWT issuance), and User Profile introspection.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models.user import User, Candidate, Recruiter
from backend.app.schemas.auth import UserRegister, UserLogin, Token, UserOut
from backend.app.utils.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email address already exists"
        )

    role = payload.role.upper()
    if role not in ("ADMIN", "CANDIDATE", "STUDENT", "RECRUITER"):
        role = "CANDIDATE"

    # Create User
    new_user = User(
        email=payload.email,
        hashed_password=get_password_hash(payload.password),
        full_name=payload.full_name,
        role=role,
    )
    db.add(new_user)
    db.flush()  # to get new_user.id

    candidate_id = None
    recruiter_id = None

    # Link Candidate or Recruiter
    if role in ("CANDIDATE", "STUDENT"):
        # Check if candidate email exists in preserved candidates table
        cand = db.query(Candidate).filter(Candidate.email == payload.email).first()
        if not cand:
            cand = Candidate(
                full_name=payload.full_name,
                email=payload.email,
                phone=payload.phone or "+91 98401 00000",
                location=payload.location or "Bengaluru, India",
                current_title=payload.current_title or "Student / Candidate",
                years_experience=0.0,
                highest_degree=payload.highest_degree or "B.Tech Computer Science",
                status="Active",
                user_id=new_user.id,
            )
            db.add(cand)
            db.flush()
        else:
            cand.user_id = new_user.id
        candidate_id = cand.id
    else:
        # Recruiter / Admin
        rec = db.query(Recruiter).filter(Recruiter.email == payload.email).first()
        if not rec:
            rec = Recruiter(
                company_id=payload.company_id or 1,
                full_name=payload.full_name,
                email=payload.email,
                role="System Admin" if role == "ADMIN" else "Technical Recruiter",
                department="Platform Operations" if role == "ADMIN" else "Talent Acquisition",
                active_requisitions=5,
                phone=payload.phone or "+91 98401 00000",
                user_id=new_user.id,
            )
            db.add(rec)
            db.flush()
        else:
            rec.user_id = new_user.id
        recruiter_id = rec.id

    db.commit()
    db.refresh(new_user)

    token = create_access_token({"sub": new_user.email, "role": new_user.role, "uid": new_user.id})
    return Token(
        access_token=token,
        token_type="bearer",
        user_id=new_user.id,
        email=new_user.email,
        full_name=new_user.full_name,
        role=new_user.role,
        candidate_id=candidate_id,
        recruiter_id=recruiter_id,
    )


@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    candidate_id = user.candidate.id if user.candidate else None
    recruiter_id = user.recruiter.id if user.recruiter else None

    # Fallback lookup in existing tables by email
    if user.role in ("STUDENT", "CANDIDATE") and not candidate_id:
        c = db.query(Candidate).filter(Candidate.email == user.email).first()
        if c:
            candidate_id = c.id
            c.user_id = user.id
            db.commit()
    elif user.role in ("RECRUITER", "ADMIN") and not recruiter_id:
        r = db.query(Recruiter).filter(Recruiter.email == user.email).first()
        if r:
            recruiter_id = r.id
            r.user_id = user.id
            db.commit()

    token = create_access_token({"sub": user.email, "role": user.role, "uid": user.id})
    return Token(
        access_token=token,
        token_type="bearer",
        user_id=user.id,
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        candidate_id=candidate_id,
        recruiter_id=recruiter_id,
    )


@router.get("/me", response_model=UserOut)
def get_me(user: User = Depends(get_current_user)):
    candidate_id = user.candidate.id if user.candidate else None
    recruiter_id = user.recruiter.id if user.recruiter else None
    return UserOut(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        created_at=user.created_at,
        candidate_id=candidate_id,
        recruiter_id=recruiter_id,
    )
