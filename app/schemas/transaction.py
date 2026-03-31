from datetime import datetime
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

class Location(BaseModel):
    lat: float
    lon: float

class Transaction(BaseModel):
    transaction_id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: str
    merchant_id: str
    amount: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    device_id: str
    location: Location | None = None
    
    # Optional field that generator injects to simulate ground truth (for demo delayed labels)
    is_fraud_simulated: bool | None = None

class TransactionLabel(BaseModel):
    transaction_id: str
    is_fraud: bool
    label_timestamp: datetime = Field(default_factory=datetime.utcnow)
