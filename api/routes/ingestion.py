import json
from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.schemas.transaction import Transaction, TransactionLabel
from app.core.config import settings
from confluent_kafka import Producer

router = APIRouter()

# Simple global producer instance for the prototype route
_producer = None

def get_producer():
    global _producer
    if _producer is None:
        _producer = Producer({'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS})
    return _producer

def produce_event(topic: str, key: str, value: dict):
    p = get_producer()
    # Serialize datetime values properly if needed, Pydantic does this nicely in .model_dump()
    p.produce(topic, key=str(key).encode(), value=json.dumps(value, default=str).encode())
    p.poll(0)

@router.post("/transaction", status_code=202)
def ingest_transaction(tx: Transaction, background_tasks: BackgroundTasks):
    """
    Ingests a raw transaction, pushing it to Redpanda for asynchronous processing.
    """
    background_tasks.add_task(produce_event, settings.TRANSACTIONS_TOPIC, tx.user_id, tx.model_dump())
    return {"status": "accepted", "transaction_id": tx.transaction_id}

@router.post("/label", status_code=202)
def ingest_label(label: TransactionLabel, background_tasks: BackgroundTasks):
    """
    Ingests a delayed label representing ground truth, useful for metric drift and retraining.
    """
    background_tasks.add_task(produce_event, settings.LABELS_TOPIC, label.transaction_id, label.model_dump())
    
    # Track purely for metrics instantly
    from monitoring.metrics import DELAYED_LABEL_FRAUD, DELAYED_LABEL_LEGIT
    if label.is_fraud:
        DELAYED_LABEL_FRAUD.inc()
        # Overwrite device risk negatively in feature store using explicit call here
        from features.store import store
        store.update_device_risk("dummy", True)  # Ideal logic grabs device_id from historical store
    else:
        DELAYED_LABEL_LEGIT.inc()
        
    return {"status": "accepted", "transaction_id": label.transaction_id}
