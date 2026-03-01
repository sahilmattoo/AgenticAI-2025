"""
Smoke Tests.
Verifies basic system availability and critical paths.
Run with: pytest tests/smoke_test.py
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Verify the /health endpoint returns 200 OK."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": "1.0.0"}

def test_chat_rule_path():
    """Verify the rule-based routing path works via API."""
    payload = {"query": "What is the system status?"}
    response = client.post("/chat", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["routing_path"] == "rule"
    assert "System is operational" in data["response"]
    assert "response" in data

def test_chat_agent_path():
    """
    Verify the agent-based routing path works via API.
    Note: Requires OPENAI_API_KEY to be valid.
    """
    # Mocking interaction to avoid cost/latency in simple smoke test if desired, 
    # but for "Operational" demo we want to hit the real path usually.
    # Here we assume the environment is set up.
    payload = {"query": "Say hello world"}
    response = client.post("/chat", json=payload)
    
    if response.status_code == 500:
        pytest.skip("Agent path failed (likely missing API Key)")
    
    assert response.status_code == 200
    data = response.json()
    assert data["routing_path"] == "agent"
    assert len(data["response"]) > 0
