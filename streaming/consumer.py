import json
import requests
from confluent_kafka import Consumer, KafkaError
from app.core.config import settings

def consume_loop():
    consumer = Consumer({
        'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS,
        'group.id': 'fraud_consumer_group',
        'auto.offset.reset': 'earliest'
    })
    
    consumer.subscribe([settings.TRANSACTIONS_TOPIC])
    print(f"Consumer started, listening to {settings.TRANSACTIONS_TOPIC}...")
    
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
                    break
                    
            event = json.loads(msg.value().decode('utf-8'))
            print(f"Consumed event: {event['transaction_id']}")
            
            # Send to API for scoring
            try:
                requests.post("http://api:8000/score", json=event, timeout=2.0)
            except Exception as e:
                print(f"Failed to call API: {e}")
                
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

if __name__ == "__main__":
    import time
    time.sleep(10) # Wait for dependent services
    consume_loop()
