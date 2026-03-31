from features.store import store
from app.schemas.transaction import Transaction

def calculate_features(tx: Transaction) -> dict:
    """
    Computes online features by merging event data with Redis state.
    """
    # 1. Get current state BEFORE this transaction
    user_feats = store.get_user_features(tx.user_id)
    device_risk = store.get_device_risk(tx.device_id)
    merchant_risk = store.get_merchant_risk(tx.merchant_id)
    shared_devices = store.get_shared_device_count(tx.user_id, tx.device_id)
    
    # 2. Extract transaction intrinsic features
    features = {
        "amount": tx.amount,
        "tx_count_1h": user_feats["tx_count_1h"],
        "tx_amount_1h": user_feats["tx_amount_1h"],
        "device_risk": device_risk,
        "merchant_risk": merchant_risk,
        "shared_device_count": shared_devices
    }
    
    # 3. Update the state asynchronously (or synchronously for the prototype)
    store.update_user_features(tx.user_id, tx.amount)
    store.link_user_to_device(tx.user_id, tx.device_id)
    
    return features
