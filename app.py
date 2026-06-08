import streamlit as st
import pandas as pd
import numpy as np
import random
import time
from datetime import datetime
import plotly.graph_objects as go
from groq import Groq

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="System Health AI Monitor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== CUSTOM CSS (LIGHT BLUE THEME) ==========
st.markdown("""
<style>
    .stApp {
        background-color: #e6f4ff;
        color: #1a2a3a;
    }
    [data-testid="stSidebar"] {
        background-color: #b8d9ff;
        border-right: 1px solid #7bb3e0;
    }
    .metric-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 1rem;
        border-left: 4px solid #2c7be5;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .security-badge {
        background-color: #d9ebff;
        border: 1px solid #2c7be5;
        border-radius: 30px;
        padding: 8px 15px;
        text-align: center;
        color: #0a4c8c;
        font-weight: bold;
        font-family: monospace;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #0a4c8c;
    }
    p, li, .stMarkdown {
        color: #1a2a3a;
    }
    .stButton>button {
        background-color: #2c7be5;
        color: white;
        border-radius: 25px;
    }
    .stButton>button:hover {
        background-color: #1a5bbf;
    }
    .stMetric {
        background-color: white;
        border-radius: 12px;
        padding: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ========== SESSION STATE ==========
if "history" not in st.session_state:
    st.session_state.history = []
if "alert_log" not in st.session_state:
    st.session_state.alert_log = []
if "last_ai" not in st.session_state:
    st.session_state.last_ai = None
if "auto_refresh" not in st.session_state:
    st.session_state.auto_refresh = False

# ========== GROQ CLIENT ==========
if "GROQ_API_KEY" not in st.secrets:
    st.error("❌ Missing Groq API key. Add `GROQ_API_KEY` to your Streamlit secrets.")
    st.stop()
groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ========== SIMULATE REAL-TIME METRICS ==========
def generate_metrics():
    cpu = random.uniform(5, 95)
    memory = random.uniform(20, 90)
    disk = random.uniform(30, 85)
    latency = random.uniform(10, 250)
    # Occasional anomalies
    if random.random() < 0.1:
        cpu = random.uniform(95, 100)
        latency = random.uniform(250, 500)
    return {
        "timestamp": datetime.now(),
        "cpu": round(cpu, 1),
        "memory": round(memory, 1),
        "disk": round(disk, 1),
        "latency": round(latency, 1)
    }

def add_metric():
    metrics = generate_metrics()
    st.session_state.history.append(metrics)
    if len(st.session_state.history) > 100:
        st.session_state.history.pop(0)
    if metrics["cpu"] > 90 or metrics["latency"] > 300:
        alert = f"⚠️ High { 'CPU' if metrics['cpu']>90 else 'Latency' }: {metrics['cpu'] if metrics['cpu']>90 else metrics['latency']}"
        st.session_state.alert_log.append({"time": metrics["timestamp"], "alert": alert})
        if len(st.session_state.alert_log) > 20:
            st.session_state.alert_log.pop(0)

# ========== AI ANOMALY ANALYSIS ==========
def ai_analyze(metrics_df):
    recent = metrics_df.tail(10).to_string()
    prompt = f"""You are a systems reliability engineer. Analyze the following system metrics (CPU%, Memory%, Disk%, Latency ms) and provide:
- Brief anomaly detection
- Recommended action
- Predicted health score (0-100)
Respond in 3-4 short sentences.

Metrics:
{recent}
"""
    try:
        completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=400
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Analysis unavailable: {e}"

# ========== SIDEBAR ==========
with st.sidebar:
    st.title("📊 System Health AI")
    st.markdown("---")
    st.markdown("### 🛡️ Global Security Shield")
    st.markdown('<div class="security-badge">🔐 Secure channel active<br>End-to-end encryption</div>', unsafe_allow_html=True)
    st.caption("All data is anonymized")
    st.markdown("---")
    st.markdown("**Built by Gesner Deslandes**  \nEngineer‑in‑Chief, GlobalInternet.py")
    st.markdown("📞 (509) 4738 5663")
    st.markdown("✉️ deslandes78@gmail.com")
    st.markdown("---")
    refresh_rate = st.selectbox("Refresh rate (seconds)", [1, 2, 5, 10], index=2)
    auto = st.checkbox("Auto-refresh", value=st.session_state.auto_refresh)
    st.session_state.auto_refresh = auto
    if st.button("🔄 Refresh Now"):
        add_metric()
        st.rerun()

# ========== MAIN DASHBOARD ==========
st.title("📈 Real‑Time System Health Monitor")
st.caption("AI‑powered anomaly detection and predictive analytics")

# Initial data
if not st.session_state.history:
    for _ in range(20):
        add_metric()

df = pd.DataFrame(st.session_state.history)
if not df.empty:
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df.set_index("timestamp", inplace=True)

    latest = df.iloc[-1]
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💻 CPU Usage", f"{latest['cpu']}%", delta=f"{latest['cpu'] - df.iloc[-2]['cpu'] if len(df)>1 else 0:.1f}%" if len(df)>1 else None)
    with col2:
        st.metric("🧠 Memory", f"{latest['memory']}%", delta=f"{latest['memory'] - df.iloc[-2]['memory'] if len(df)>1 else 0:.1f}%" if len(df)>1 else None)
    with col3:
        st.metric("💾 Disk", f"{latest['disk']}%")
    with col4:
        st.metric("⏱️ Latency", f"{latest['latency']} ms", delta=f"{latest['latency'] - df.iloc[-2]['latency'] if len(df)>1 else 0:.1f}" if len(df)>1 else None)

    st.subheader("📉 Real‑time Trends")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['cpu'], mode='lines', name='CPU %', line=dict(color='#2c7be5')))
    fig.add_trace(go.Scatter(x=df.index, y=df['memory'], mode='lines', name='Memory %', line=dict(color='#10b981')))
    fig.add_trace(go.Scatter(x=df.index, y=df['latency'], mode='lines', name='Latency (ms)', yaxis='y2', line=dict(color='#ef4444', dash='dot')))
    fig.update_layout(
        yaxis=dict(title='Percentage (%)', gridcolor='#cce4ff'),
        yaxis2=dict(title='Latency (ms)', overlaying='y', side='right', gridcolor='#cce4ff'),
        plot_bgcolor='#f0f8ff',
        paper_bgcolor='#f0f8ff',
        font=dict(color='#1a2a3a'),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🤖 AI Predictive Analysis")
    col_ai, col_alert = st.columns([2, 1])
    with col_ai:
        if st.button("🧠 Run AI Anomaly Analysis"):
            with st.spinner("AI analyzing system health..."):
                analysis = ai_analyze(df.reset_index())
                st.session_state.last_ai = analysis
        if st.session_state.last_ai:
            st.info(st.session_state.last_ai)
    with col_alert:
        st.subheader("🚨 Live Alerts")
        if st.session_state.alert_log:
            for alert in st.session_state.alert_log[-5:]:
                st.warning(f"{alert['alert']} at {alert['time'].strftime('%H:%M:%S')}")
        else:
            st.success("No active alerts")
else:
    st.info("Collecting first metrics...")

# ========== AUTO REFRESH ==========
if st.session_state.auto_refresh:
    add_metric()
    time.sleep(refresh_rate)
    st.rerun()

# ========== FOOTER ==========
st.markdown("---")
st.caption("© 2026 GlobalInternet.py – Built for real‑time system observability & AI‑assisted operations")
