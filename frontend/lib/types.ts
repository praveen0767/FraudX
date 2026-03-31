export interface Transaction {
  transaction_id: string;
  user_id: string;
  amount: number;
  merchant: string;
  device_id: string;
  location: string | null;
  timestamp: string;
  fraud_score?: number;
  decision?: "APPROVE" | "REVIEW" | "BLOCK";
  status?: string;
  is_fraud_simulated?: boolean;
}

export interface DecisionDetail {
  transaction_id: string;
  fraud_score: number;
  decision: string;
  explanation: string;
  top_features: { name: string; value: number }[];
  shap_values?: { feature: string; impact: number }[];
  model_breakdown: {
    base_model: number;
    contextual_agent?: number;
    final_score: number;
  };
  contextual_agent?: {
    triggered: boolean;
    reasoning: string;
    confidence: number;
  };
  latency_ms: number;
  model_version?: string;
}

export interface Metrics {
  throughput: number;
  latency_p95: number;
  error_rate: number;
  drift_score: number;
  model_version: string;
}

// Adapted from Python Backend (Legacy mapping if needed)
export interface BackendDecisionResult {
  transaction_id: string;
  fraud_score: number;
  decision: string;
  explanation: string;
  top_features: Record<string, number>;
  risk_reasons?: { feature: string; impact: string; description: string }[];
  model_version: string;
  processing_latency_ms: number;
  agent_triggered: boolean;
}
