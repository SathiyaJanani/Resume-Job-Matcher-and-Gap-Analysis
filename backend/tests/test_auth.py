"""
Unit tests for Authentication & Authorization in SkillBridge AI.
"""

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_register_student():
    import uuid
    unique_email = f"student_{uuid.uuid4().hex[:6]}@test.edu"
    payload = {
        "email": unique_email,
        "password": "SecretPassword123!",
        "full_name": "Test Student User",
        "role": "STUDENT",
        "phone": "+91 99999 88888",
        "location": "Chennai, India",
        "current_title": "Final Year CSE Student",
        "highest_degree": "B.Tech Computer Science",
    }
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["role"] == "STUDENT"
    assert data["email"] == unique_email
    assert data["candidate_id"] is not None


def test_login_valid_and_invalid():
    # Login with known seeded student
    res_valid = client.post("/api/auth/login", json={
        "email": "student@skillbridge.ai",
        "password": "password123"
    })
    assert res_valid.status_code == 200
    token_data = res_valid.json()
    assert "access_token" in token_data
    assert token_data["role"] == "STUDENT"

    # Login with wrong password
    res_invalid = client.post("/api/auth/login", json={
        "email": "student@skillbridge.ai",
        "password": "wrong_password_xyz"
    })
    assert res_invalid.status_code == 401


def test_get_current_user_me():
    # 1. Login
    res_login = client.post("/api/auth/login", json={
        "email": "recruiter@nexusai.io",
        "password": "recruiter123"
    })
    assert res_login.status_code == 200
    token = res_login.json()["access_token"]

    # 2. Get profile with Bearer Token
    res_me = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res_me.status_code == 200
    user_info = res_me.json()
    assert user_info["email"] == "recruiter@nexusai.io"
    assert user_info["role"] == "RECRUITER"


def test_protected_route_unauthorized():
    res = client.get("/api/auth/me")
    assert res.status_code == 401
