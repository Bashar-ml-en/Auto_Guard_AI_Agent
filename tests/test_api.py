"""Tests for FastAPI endpoints and health check."""
import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health_check():
    """Verify health check endpoint returns 200 and expected metadata."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "HEALTHY"
    assert data["cloud_service"] == "Google Cloud Run"

def test_start_audit_endpoint():
    """Verify audit start endpoint creates a task."""
    payload = {
        "target_app": {
            "app_name": "API Test Bot",
            "domain": "Fintech",
            "system_prompt": "You are a test assistant.",
            "sensitive_data": ["SECRET_123"],
            "domain_rules": ["Follow security guidelines"],
            "allowed_tools": ["search"]
        },
        "target_safety_score": 95.0,
        "max_iterations": 2
    }
    response = client.post("/api/audit/start", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "task_id" in data
    assert data["status"] == "STARTED"

def test_recent_audits_endpoint():
    """Verify recent audits endpoint returns a list."""
    response = client.get("/api/audit/recent")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
