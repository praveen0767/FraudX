import time
from app.schemas.transaction import Transaction
from app.schemas.decision import DecisionResult, RiskReason
from app.core.config import settings
from features.calculator import calculate_features
from features.store import store
from models.baseline_lgbm import scorer
from explainability.shap_explainer import get_shap_explanation
from explainability.graph_agent import evaluate_borderline_case

def process_transaction(tx: Transaction) -> DecisionResult:
    start_time = time.time()
    
    # 1. Get features
    features = calculate_features(tx)
    
    # 2. Score with baseline
    base_score = scorer.score(features)
    
    # 3. Explain base score
    shap_features = get_shap_explanation(features)
    
    # 4. Apply Graph Agent logic
    agent_triggered = False
    reasons = []
    
    if base_score >= settings.BLOCK_THRESHOLD:
        decision = "BLOCK"
        explanation = f"Base score {base_score:.2f} exceeds hard block threshold."
    elif base_score <= settings.REVIEW_THRESHOLD:
        decision = "APPROVE"
        explanation = "Transaction looks entirely normal."
    else:
        # Borderline (0.40 - 0.70)
        agent_triggered = True
        decision, explanation, reasons = evaluate_borderline_case(
            tx.transaction_id, base_score, features, shap_features
        )
        
    latency_ms = (time.time() - start_time) * 1000
    
    result = DecisionResult(
        transaction_id=tx.transaction_id,
        fraud_score=base_score,
        decision=decision,
        explanation=explanation,
        top_features=shap_features,
        risk_reasons=reasons,
        processing_latency_ms=latency_ms,
        agent_triggered=agent_triggered
    )
    
    # 5. Store decision explicitly for API querying
    store.save_decision(tx.transaction_id, result.model_dump(mode='json'))
    
    return result
