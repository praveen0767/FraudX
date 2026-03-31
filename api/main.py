from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
import time

from api.routes import ingestion, scoring
from monitoring.metrics import REQUEST_COUNT, REQUEST_LATENCY
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Real-time Fraud MVP supporting streaming, SHAP explanations, and Graph Contextual Agents."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prometheus endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Global metrics middleware
@app.middleware("http")
async def add_prometheus_metrics(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    latency = time.time() - start_time
    
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
    REQUEST_LATENCY.labels(method=request.method, endpoint=request.url.path).observe(latency)
    
    return response

# Health checkpoint
@app.get("/health")
def health_check():
    return {"status": "ok", "timestamp": time.time()}

# Routers
app.include_router(ingestion.router, tags=["Ingestion"])
app.include_router(scoring.router, tags=["Scoring"])
