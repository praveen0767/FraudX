import pytest
from app.schemas.transaction import Transaction
from models.baseline_lgbm import scorer
from explainability.graph_agent import evaluate_borderline_case
from explainability.shap_explainer import get_shap_explanation

def test_model_inference():
    features = {
        "amount": 500.0,
        "tx_count_1h": 5,
        "tx_amount_1h": 2000.0,
        "device_risk": 0.5,
        "merchant_risk": 0.1,
        "shared_device_count": 2
    }
    score = scorer.score(features)
    assert 0.0 <= score <= 1.0

def test_shap_explanation():
    features = {"amount": 50.0, "tx_count_1h": 1}
    shap_vals = get_shap_explanation(features)
    assert isinstance(shap_vals, dict)
    assert len(shap_vals) == 6 # Total defined features
    assert "amount" in shap_vals

def test_agent_fallback_logic():
    features = {
        "amount": 2000.0, 
        "tx_count_1h": 5,
        "device_risk": 0.8,
        "shared_device_count": 3
    }
    shap = {"amount": 1.2, "device_risk": 0.9}
    
    decision, explanation, reasons = evaluate_borderline_case("tx-1", 0.65, features, shap)
    
    # Based on our deterministic rules, this should be BLOCK
    assert decision == "BLOCK"
    assert len(reasons) > 0
    assert reasons[0].feature in ["device_linkage", "velocity_amount"]
