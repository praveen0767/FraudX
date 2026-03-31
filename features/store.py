import json
import redis
from app.core.config import settings

class FeatureStore:
    def __init__(self):
        self.client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)

    def get_user_features(self, user_id: str) -> dict:
        data = self.client.hgetall(f"user:{user_id}")
        return {
            "tx_count_1h": int(data.get("tx_count_1h", 0)),
            "tx_amount_1h": float(data.get("tx_amount_1h", 0.0)),
        }

    def update_user_features(self, user_id: str, amount: float):
        key = f"user:{user_id}"
        self.client.hincrby(key, "tx_count_1h", 1)
        self.client.hincrbyfloat(key, "tx_amount_1h", amount)
        self.client.expire(key, 3600)  # TTL of 1 hour

    def get_device_risk(self, device_id: str) -> float:
        risk_score = self.client.get(f"device_risk:{device_id}")
        return float(risk_score) if risk_score else 0.0

    def update_device_risk(self, device_id: str, is_fraud: bool):
        # Extremely simplified device risk tracking for demo
        key = f"device_risk:{device_id}"
        current_risk = self.get_device_risk(device_id)
        if is_fraud:
            new_risk = min(current_risk + 0.5, 1.0)
        else:
            new_risk = max(current_risk - 0.1, 0.0)
        self.client.set(key, new_risk, ex=86400) # 1 day TTL
        
    def link_user_to_device(self, user_id: str, device_id: str):
        # Graph feature: tracking which users have used which devices
        self.client.sadd(f"device_users:{device_id}", user_id)
        self.client.sadd(f"user_devices:{user_id}", device_id)
        
    def get_shared_device_count(self, user_id: str, device_id: str) -> int:
        users = self.client.smembers(f"device_users:{device_id}")
        return len(users)

    def get_merchant_risk(self, merchant_id: str) -> float:
        risk = self.client.get(f"merchant_risk:{merchant_id}")
        return float(risk) if risk else 0.1

    def save_decision(self, transaction_id: str, decision_data: dict):
        flattened_data = {}
        for k, v in decision_data.items():
            if isinstance(v, (dict, list)):
                flattened_data[k] = json.dumps(v)
            else:
                flattened_data[k] = str(v)
        self.client.hset(f"decision:{transaction_id}", mapping=flattened_data)
        self.client.expire(f"decision:{transaction_id}", 86400 * 7) # 7 days
        
    def get_decision(self, transaction_id: str) -> dict:
        data = self.client.hgetall(f"decision:{transaction_id}")
        if not data: return data
        for k in ["top_features", "risk_reasons"]:
            if k in data and isinstance(data[k], str) and data[k].startswith(("{", "[")):
                try: data[k] = json.loads(data[k])
                except: pass
        return data

store = FeatureStore()
