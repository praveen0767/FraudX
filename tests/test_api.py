from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_metrics_endpoint():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "request_count" in response.text

def test_score_transaction():
    payload = {
        "transaction_id": "test-id-123",
        "user_id": "U123",
        "merchant_id": "M123",
        "amount": 100.0,
        "timestamp": "2026-03-31T20:00:00Z",
        "device_id": "D123"
    }
    response = client.post("/score", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "fraud_score" in data
    assert data["decision"] in ["APPROVE", "REVIEW", "BLOCK"]
    assert "explanation" in data
