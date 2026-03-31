import requests
from app.core.config import settings
from app.schemas.decision import RiskReason

def evaluate_borderline_case(tx_id: str, score: float, features: dict, shap_features: dict) -> tuple[str, str, list[RiskReason]]:
    """
    Determines final outcome using Groq/OpenAI if available, else falls back to a deterministic rules engine.
    """
    reasons = []
    
    # 1. Fallback deterministic rules engine (always works for demo)
    decision = "REVIEW"
    explanation = f"Base score {score:.2f} is ambiguous. Manual review required."
    
    # Identify top drivers via SHAP
    top_driver = list(shap_features.keys())[0] if shap_features else "amount"
    
    if features.get("shared_device_count", 0) > 1 and features.get("device_risk", 0.0) > 0.4:
        decision = "BLOCK"
        explanation = "Contextual Graph Agent elevated risk to BLOCK: User device is linked to multiple other unique users and exhibits elevated historical risk."
        reasons.append(RiskReason(feature="device_linkage", impact="HIGH", description="Device shared across multiple distinct accounts."))
        
    elif features.get("amount", 0) > 1000 and features.get("tx_count_1h", 0) > 3:
        decision = "BLOCK"
        explanation = "Contextual Agent elevated risk to BLOCK: High uncharacteristic velocity clustered with large nominal amount."
        reasons.append(RiskReason(feature="velocity_amount", impact="HIGH", description="High transaction volume within 1 hour."))
        
    elif score < 0.55 and features.get("device_risk", 1.0) < 0.1:
        decision = "APPROVE"
        explanation = "Contextual Agent lowered risk to APPROVE: Despite anomalies, device history is extremely clean."
        reasons.append(RiskReason(feature="safe_device", impact="LOW", description="Device has long history of legitimate transactions."))
        
    # 2. Try LLM if configured
    if settings.GROQ_API_KEY:
        try:
            headers = {"Authorization": f"Bearer {settings.GROQ_API_KEY}"}
            prompt = f"Analyze this borderline transaction ({score=:.2f}). Features: {features}. Top SHAP: {shap_features}. Decide 'APPROVE', 'REVIEW', or 'BLOCK'. Return JSON: {{'decision': '...', 'explanation': '...', 'reasons': [...]}}"
            payload = {
                "model": "llama3-8b-8192",
                "messages": [{"role": "system", "content": "You are a fraud analyst."}, {"role": "user", "content": prompt}],
                "response_format": {"type": "json_object"}
            }
            resp = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=2.0)
            if resp.status_code == 200:
                data = resp.json()["choices"][0]["message"]["content"]
                parsed = eval(data) # In production use json.loads
                return parsed.get("decision", decision).upper(), parsed.get("explanation", explanation), reasons
        except Exception as e:
            print(f"LLM Agent failed, using fallback: {e}")
            
    return decision, explanation, reasons
