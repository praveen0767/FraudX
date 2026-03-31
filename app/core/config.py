from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Real-Time Contextual Fraud Detection"
    VERSION: str = "1.0.0"
    
    # Redpanda/Kafka
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    TRANSACTIONS_TOPIC: str = "transactions"
    LABELS_TOPIC: str = "delayed_labels"
    
    # Redis (Feature Store)
    REDIS_URL: str = "redis://localhost:6379"
    
    # Agent APIs
    GROQ_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    
    # Scoring Thresholds
    BLOCK_THRESHOLD: float = 0.70
    REVIEW_THRESHOLD: float = 0.40  # Scores between 0.40 and 0.70 trigger the Agent
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
