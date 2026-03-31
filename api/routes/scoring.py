import json
from fastapi import APIRouter, HTTPException
from app.schemas.transaction import Transaction
from app.schemas.decision import DecisionResult
from api.services import process_transaction
from features.store import store
from monitoring.metrics import FRAUD_SCORE_DISTRIBUTION, DECISION_COUNT, AGENT_INVOCATIONS

router = APIRouter()

@router.post("/score", response_model=DecisionResult)
def score_transaction(tx: Transaction):
    """
    Synchronous scoring endpoint. Real systems usually run this in the consumer async, 
    but an API is useful for testing, immediate checkout blocking, and the Streamlit demo.
    """
    result = process_transaction(tx)
    
    # Emit domain metrics
    FRAUD_SCORE_DISTRIBUTION.observe(result.fraud_score)
    DECISION_COUNT.labels(decision_type=result.decision).inc()
    if result.agent_triggered:
        AGENT_INVOCATIONS.inc()
        
    return result

@router.get("/decision/{transaction_id}", response_model=DecisionResult)
def get_decision(transaction_id: str):
    """
    Fetch a decision by ID from Redis.
    """
    data = store.get_decision(transaction_id)
    if not data:
        raise HTTPException(status_code=404, detail="Decision not found")
        
    # Reconstruct back
    data["fraud_score"] = float(data["fraud_score"])
    data["processing_latency_ms"] = float(data["processing_latency_ms"])
    data["agent_triggered"] = data["agent_triggered"] == "True"
    
    # Deserialize nested dictionary/list from strings
    if "top_features" in data and isinstance(data["top_features"], str):
        data["top_features"] = json.loads(data["top_features"])
    if "risk_reasons" in data and isinstance(data["risk_reasons"], str):
        data["risk_reasons"] = json.loads(data["risk_reasons"])
    
    return data

@router.get("/explain/{transaction_id}")
def explain_decision(transaction_id: str):
    """
    Fetch raw SHAP details or Agent logs.
    """
    data = store.get_decision(transaction_id)
    if not data:
        raise HTTPException(status_code=404, detail="Decision not found")
        
    return {
        "transaction_id": transaction_id,
        "explanation": data.get("explanation", ""),
        "top_features": data.get("top_features", "{}"),
        "risk_reasons": data.get("risk_reasons", "[]")
    }
