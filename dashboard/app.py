import streamlit as st
import requests
import json
import time
import uuid
import random
from datetime import datetime
import plotly.express as px
import pandas as pd

API_URL = "http://api:8000"

st.set_page_config(page_title="Fraud MVP Dashboard", layout="wide")
st.title("Real-Time Contextual Fraud Detection")
st.markdown("Live demo of streaming ingestion, LightGBM base scoring, and Graph Agent contextual reasoning.")

# Sidebar Controls
st.sidebar.header("Demo Simulation")

def generate_payload(fraud_type="normal"):
    amount = round(random.uniform(10.0, 100.0), 2)
    device_id = f"DEV_{random.randint(1000, 9000)}"
    user_id = f"U{random.randint(100, 900)}"
    
    if fraud_type == "fraud":
        amount = round(random.uniform(2000.0, 5000.0), 2)
        device_id = "DEV_0099" # Known bad
        user_id = "U0099"
    elif fraud_type == "borderline":
        amount = round(random.uniform(800.0, 1500.0), 2)
        device_id = "DEV_0099" # Induces Graph linkage

    return {
        "transaction_id": str(uuid.uuid4()),
        "user_id": user_id,
        "merchant_id": f"M{random.randint(10, 50)}",
        "amount": amount,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "device_id": device_id,
        "location": {"lat": 34.0, "lon": -118.0}
    }

def send_transaction(payload):
    try:
        start = time.time()
        resp = requests.post(f"{API_URL}/score", json=payload, timeout=5.0)
        latency = (time.time() - start) * 1000
        if resp.status_code == 200:
            return resp.json(), latency
        else:
            st.error(f"API Error: {resp.text}")
    except requests.exceptions.RequestException as e:
        st.sidebar.error(f"Connection failed: {e}")
    return None, 0.0

trigger_normal = st.sidebar.button("Normal Tx", use_container_width=True)
trigger_borderline = st.sidebar.button("Borderline Tx", use_container_width=True)
trigger_fraud = st.sidebar.button("Fraud Tx", use_container_width=True)

if trigger_normal: st.session_state.current_tx = generate_payload("normal")
if trigger_borderline: st.session_state.current_tx = generate_payload("borderline")
if trigger_fraud: st.session_state.current_tx = generate_payload("fraud")

if "current_tx" in st.session_state:
    tx = st.session_state.current_tx
    
    result, round_trip_latency = send_transaction(tx)
    if result:
        # Layout View
        c1, c2, c3 = st.columns(3)
        
        c1.metric("Risk Score", f"{result['fraud_score']:.2f}")
        c2.metric("Decision", result['decision'])
        c3.metric("Processing Latency", f"{result['processing_latency_ms']:.1f} ms")
        
        st.subheader("Transaction Details")
        st.json(tx)
        
        st.subheader("Explanation")
        if result['agent_triggered']:
            st.warning("⚠️ Contextual Graph Agent Triggered (Borderline Case)")
        st.info(result['explanation'])
        
        if result['risk_reasons']:
            for reason in result['risk_reasons']:
                st.write(f"- **{reason['feature']}** ({reason['impact']}): {reason['description']}")
                
        # SHAP Importance Plot
        st.subheader("Feature Impacts (SHAP)")
        top_features = result.get('top_features', {})
        if top_features:
            df = pd.DataFrame(list(top_features.items()), columns=['Feature', 'SHAP Value'])
            df = df.sort_values(by='SHAP Value', ascending=True)
            
            # Simple bar chart
            fig = px.bar(df, x='SHAP Value', y='Feature', orientation='h', title="Why this decision was made")
            st.plotly_chart(fig, use_container_width=True)
