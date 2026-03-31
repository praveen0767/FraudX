import time
import json
import random
import uuid
from datetime import datetime
from confluent_kafka import Producer
from app.core.config import settings

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")

def generate_transactions(num_events=1000, delay=0.1):
    producer = Producer({'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS})
    
    users = [f"U{i:04d}" for i in range(100)]
    merchants = [f"M{i:03d}" for i in range(20)]
    devices = [f"DEV_{i:04d}" for i in range(150)]
    
    fraudsters = ["U0099", "U0088"]
    fraud_devices = ["DEV_0099", "DEV_0088"]
    
    print(f"Starting transaction generation towards {settings.KAFKA_BOOTSTRAP_SERVERS}...")
    
    for i in range(num_events):
        is_borderline = random.random() < 0.1
        is_fraud = random.random() < 0.05
        
        user_id = random.choice(users)
        merchant_id = random.choice(merchants)
        device_id = random.choice(devices)
        amount = round(random.uniform(5.0, 500.0), 2)
        
        if is_fraud:
            user_id = random.choice(fraudsters)
            device_id = random.choice(fraud_devices)
            amount = round(random.uniform(1000.0, 5000.0), 2)
        elif is_borderline:
            # Force high amount and weird device intersection to trigger agent
            amount = round(random.uniform(800.0, 1500.0), 2)
            device_id = random.choice(fraud_devices)
            
        tx = {
            "transaction_id": str(uuid.uuid4()),
            "user_id": user_id,
            "merchant_id": merchant_id,
            "amount": amount,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "device_id": device_id,
            "location": {"lat": round(random.uniform(30.0, 45.0), 4), "lon": round(random.uniform(-120.0, -70.0), 4)},
            "is_fraud_simulated": is_fraud
        }
        
        producer.produce(
            settings.TRANSACTIONS_TOPIC,
            key=tx["user_id"].encode('utf-8'),
            value=json.dumps(tx).encode('utf-8'),
            callback=delivery_report
        )
        producer.poll(0)
        time.sleep(delay)
        
    producer.flush()
    print("Generation complete.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=100000)
    parser.add_argument("--delay", type=float, default=1.0)
    args = parser.parse_args()
    
    # Wait for Kafka to be ready
    time.sleep(5)
    generate_transactions(args.count, args.delay)
