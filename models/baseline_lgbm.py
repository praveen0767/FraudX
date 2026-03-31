import os
import numpy as np
import lightgbm as lgb
from models.trainer import train_dummy_model

MODEL_PATH = "data/model.txt"

class FraudScorer:
    def __init__(self):
        if not os.path.exists(MODEL_PATH):
            train_dummy_model()
        self.model = lgb.Booster(model_file=MODEL_PATH)

    def score(self, features: dict) -> float:
        """
        Takes raw feature dictionary, outputs fraud prob.
        """
        # Order must match training
        ordered_features = [
            features.get("amount", 0.0),
            features.get("tx_count_1h", 0),
            features.get("tx_amount_1h", 0.0),
            features.get("device_risk", 0.0),
            features.get("merchant_risk", 0.1),
            features.get("shared_device_count", 0)
        ]
        
        preds = self.model.predict(np.array([ordered_features]))
        return float(preds[0])

scorer = FraudScorer()
