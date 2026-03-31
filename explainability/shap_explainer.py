import numpy as np
import shap
from models.baseline_lgbm import scorer

# We employ TreeExplainer for LightGBM
explainer = shap.TreeExplainer(scorer.model)

def get_shap_explanation(features: dict) -> dict:
    """
    Given a feature dictionary, return the SHAP values sorted by absolute impact.
    """
    feature_names = [
        "amount", "tx_count_1h", "tx_amount_1h", 
        "device_risk", "merchant_risk", "shared_device_count"
    ]
    
    ordered_features = np.array([[
        features.get("amount", 0.0),
        features.get("tx_count_1h", 0),
        features.get("tx_amount_1h", 0.0),
        features.get("device_risk", 0.0),
        features.get("merchant_risk", 0.1),
        features.get("shared_device_count", 0)
    ]])
    
    shap_values = explainer.shap_values(ordered_features)[1] if isinstance(explainer.shap_values(ordered_features), list) else explainer.shap_values(ordered_features)
    # SHAP outputs can be slightly different depending on version, handle single output vs list
    if len(np.shape(shap_values)) == 3:
        shap_values = shap_values[0][:, 1] # Binary classification indexing
    elif len(np.shape(shap_values)) == 2:
        shap_values = shap_values[0]
    else:
        shap_values = np.ravel(shap_values)
        
    contributions = {name: float(val) for name, val in zip(feature_names, shap_values)}
    
    # Sort by absolute impact
    sorted_contributions = dict(sorted(contributions.items(), key=lambda item: abs(item[1]), reverse=True))
    return sorted_contributions
