from prometheus_client import Counter, Histogram

# General Application Metrics
REQUEST_COUNT = Counter(
    "request_count", "Total HTTP requests", ["method", "endpoint"]
)

REQUEST_LATENCY = Histogram(
    "request_latency_seconds", "HTTP request latency", ["method", "endpoint"]
)

# Domain Specific Metrics
FRAUD_SCORE_DISTRIBUTION = Histogram(
    "fraud_score", "Distribution of base fraud scores", buckets=(0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0)
)

DECISION_COUNT = Counter(
    "decision_count", "Count of decisions by type", ["decision_type"]
)

AGENT_INVOCATIONS = Counter(
    "agent_invocations_total", "Number of times the Graph Agent was triggered"
)

# Used to track labels vs scores over time
DELAYED_LABEL_FRAUD = Counter(
    "delayed_label_fraud", "Count of true fraud labels received"
)
DELAYED_LABEL_LEGIT = Counter(
    "delayed_label_legit", "Count of true legit labels received"
)
