import os
import json
import numpy as np
import lightgbm as lgb
from sklearn.datasets import make_classification

MODEL_PATH = "data/model.txt"

def train_dummy_model():
    os.makedirs("data", exist_ok=True)
    print("Training synthetic baseline fraud model...")
    
    # 5 Features: amount, tx_count_1h, tx_amount_1h, device_risk, merchant_risk
    # We add 1 for shared_device_count
    
    X, y = make_classification(
        n_samples=5000, 
        n_features=6, 
        n_informative=4, 
        n_redundant=0, 
        random_state=42, 
        weights=[0.95, 0.05]
    )
    
    # Let's map features nicely so SHAP looks realistic
    # F0: amount
    # F1: tx_count_1h
    # F2: tx_amount_1h
    # F3: device_risk
    # F4: merchant_risk
    # F5: shared_device_count
    
    train_data = lgb.Dataset(X, label=y, feature_name=[
        "amount", "tx_count_1h", "tx_amount_1h", 
        "device_risk", "merchant_risk", "shared_device_count"
    ])
    
    params = {
        "objective": "binary",
        "metric": "auc",
        "boosting_type": "gbdt",
        "learning_rate": 0.05,
        "num_leaves": 31,
        "verbose": -1
    }
    
    model = lgb.train(params, train_data, num_boost_round=100)
    model.save_model(MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train_dummy_model()
