"""
Pydantic schemas for Authentication and User management.
"""

from typing import Optional
from pydantic import BaseModel, ConfigDict


class UserRegister(BaseModel):
    email: str
    password: str
    full_name: str
    role: str = "STUDENT"  # 'STUDENT' or 'RECRUITER'
    phone: Optional[str] = "+91 98401 00000"
    location: Optional[str] = "Bengaluru, India"
    current_title: Optional[str] = "Student / Aspiring Software Engineer"
    highest_degree: Optional[str] = "B.Tech Computer Science"
    company_id: Optional[int] = 1


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    email: str
    full_name: str
    role: str
    candidate_id: Optional[int] = None
    recruiter_id: Optional[int] = None


class UserOut(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    created_at: str
    candidate_id: Optional[int] = None
    recruiter_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
