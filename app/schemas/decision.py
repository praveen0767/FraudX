from pydantic import BaseModel
from typing import Dict, Any, List

class RiskReason(BaseModel):
    feature: str
    impact: str
    description: str

class DecisionResult(BaseModel):
    transaction_id: str
    fraud_score: float
    decision: str  # "APPROVE", "REVIEW" (Agent), "BLOCK"
    explanation: str
    top_features: Dict[str, float]
    risk_reasons: List[RiskReason] = []
    model_version: str = "v1"
    processing_latency_ms: float = 0.0
    agent_triggered: bool = False
