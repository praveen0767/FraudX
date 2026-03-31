# Real-Time Contextual Fraud Detection MVP

This repository contains the prototype for the **FinTech-1** hackathon challenge. 
It implements a real-time event-driven fraud detection system utilizing a baseline Machine Learning model (LightGBM) enhanced by a novel "Real-Time Contextual Graph Agent" for navigating borderline decisions. 

## Novel Innovation

Most real-time fraud engines rely purely on static thresholds, struggling with borderline (0.4 - 0.7 risk) grey-area transactions.
**Our contribution:** Instead of blocking outright or blindly approving, our pipeline intercepts borderline scores and hands them off to the **Contextual Graph Agent**. This semantic agent evaluates:
1. Feature Impacts via native SHAP values.
2. Real-time Node linkages (Has this device been shared across multiple distinct users today?)
3. Velocity clusters.

It returns a deterministic, highly-explainable sub-decision (`APPROVE`, `REVIEW`, `BLOCK`) directly to the API in milliseconds. (If initialized with a `GROQ_API_KEY`, it routes logic through an LLM; otherwise, it relies on an embedded deterministic fallback engine to guarantee demo availability).

## Architecture

- **Ingestion:** Redpanda (Kafka-compatible) for highly concurrent asynchronous streaming events.
- **Micro-batch Cache / Feature Store:** Redis Hash Maps for sub-millisecond graph and velocity tracking.
- **Scoring Engine:** Pre-trained LightGBM Booster and SHAP TreeExplainer.
- **Reasoning Layer:** Contextual Graph Agent.
- **API:** FastAPI.
- **Monitoring:** Prometheus application instrumentation.
- **UI:** Streamlit interactive demo dashboard.

## Quickstart

Run the entire cluster locally using Docker Compose.

```bash
docker-compose up --build -d
```

### Services
- **Dashboard (UI):** [http://localhost:8501](http://localhost:8501)
- **API Swagger Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Prometheus Metrics:** [http://localhost:8000/metrics](http://localhost:8000/metrics)

## Live Demo Script (1-Minute Flow)

1. Open [http://localhost:8501](http://localhost:8501).
2. Click **"Normal Tx"**. Note the low Base Risk Score, "APPROVE" decision, and clean SHAP chart.
3. Click **"Fraud Tx"**. Note the extremely high Risk Score ( > 0.7), the immediate "BLOCK" status without agent interference, and the amount/velocity dominance in the graph.
4. Click **"Borderline Tx"**. Note the mid-range Risk Score. **Watch as the semantic interface triggers the Contextual Graph Agent** to evaluate device linkages, eventually updating the status with a clear, human-readable graph reasoning string.

## Roadmap
- Integrate Neo4J natively for multi-hop neighborhood features instead of simple Redis Sets.
- Replace dummy dataset with Kaggle IEEE-CIS tabular data.
- Wire up Grafana directly to the scraping `/metrics` Prom endpoint.
