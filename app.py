import streamlit as st
import pandas as pd
import numpy as np
import random
import time
import asyncio
import tempfile
import os
from datetime import datetime
import plotly.graph_objects as go
from groq import Groq
import edge_tts

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="System Health AI Monitor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== LANGUAGE DICTIONARIES ==========
TEXTS = {
    "English": {
        "title": "📈 Real‑Time System Health Monitor",
        "caption": "AI‑powered anomaly detection and predictive analytics",
        "cpu": "💻 CPU Usage",
        "memory": "🧠 Memory",
        "disk": "💾 Disk",
        "latency": "⏱️ Latency",
        "trends": "📉 Real‑time Trends",
        "ai_title": "🤖 AI Predictive Analysis",
        "run_ai": "🧠 Run AI Anomaly Analysis",
        "ai_thinking": "AI analyzing system health...",
        "ai_unavailable": "Analysis temporarily unavailable",
        "alerts_title": "🚨 Live Alerts",
        "no_alerts": "No active alerts",
        "refresh_rate": "Refresh rate (seconds)",
        "auto_refresh": "Auto-refresh",
        "refresh_now": "🔄 Refresh Now",
        "security_badge": "🔐 Secure channel active",
        "security_caption": "End-to-end encryption",
        "explain_btn": "🎙️ AI Voice Explanation",
        "explain_playing": "Playing explanation...",
        "explain_error": "Could not generate voice. Please try again.",
        "generating_audio": "Generating voice...",
        "footer": "© 2026 GlobalInternet.py – Built for real‑time system observability & AI‑assisted operations"
    },
    "French": {
        "title": "📈 Moniteur de santé système en temps réel",
        "caption": "Détection d'anomalies et analyses prédictives par IA",
        "cpu": "💻 Utilisation CPU",
        "memory": "🧠 Mémoire",
        "disk": "💾 Disque",
        "latency": "⏱️ Latence",
        "trends": "📉 Tendances en temps réel",
        "ai_title": "🤖 Analyse prédictive IA",
        "run_ai": "🧠 Lancer l'analyse d'anomalies",
        "ai_thinking": "L'IA analyse l'état du système...",
        "ai_unavailable": "Analyse temporairement indisponible",
        "alerts_title": "🚨 Alertes en direct",
        "no_alerts": "Aucune alerte active",
        "refresh_rate": "Fréquence de rafraîchissement (secondes)",
        "auto_refresh": "Rafraîchissement auto",
        "refresh_now": "🔄 Rafraîchir maintenant",
        "security_badge": "🔐 Canal sécurisé actif",
        "security_caption": "Chiffrement de bout en bout",
        "explain_btn": "🎙️ Explication vocale IA",
        "explain_playing": "Lecture de l'explication...",
        "explain_error": "Impossible de générer la voix. Réessayez.",
        "generating_audio": "Génération de la voix...",
        "footer": "© 2026 GlobalInternet.py – Conçu pour l'observabilité système et les opérations assistées par IA"
    },
    "Spanish": {
        "title": "📈 Monitor de salud del sistema en tiempo real",
        "caption": "Análisis predictivo y detección de anomalías con IA",
        "cpu": "💻 Uso de CPU",
        "memory": "🧠 Memoria",
        "disk": "💾 Disco",
        "latency": "⏱️ Latencia",
        "trends": "📉 Tendencias en tiempo real",
        "ai_title": "🤖 Análisis predictivo IA",
        "run_ai": "🧠 Ejecutar análisis de anomalías",
        "ai_thinking": "IA analizando el estado del sistema...",
        "ai_unavailable": "Análisis temporalmente no disponible",
        "alerts_title": "🚨 Alertas en vivo",
        "no_alerts": "No hay alertas activas",
        "refresh_rate": "Frecuencia de actualización (segundos)",
        "auto_refresh": "Actualización automática",
        "refresh_now": "🔄 Actualizar ahora",
        "security_badge": "🔐 Canal seguro activo",
        "security_caption": "Cifrado de extremo a extremo",
        "explain_btn": "🎙️ Explicación por voz IA",
        "explain_playing": "Reproduciendo explicación...",
        "explain_error": "No se pudo generar la voz. Intente de nuevo.",
        "generating_audio": "Generando voz...",
        "footer": "© 2026 GlobalInternet.py – Construido para observabilidad de sistemas y operaciones asistidas por IA"
    }
}

# ========== VOICE MAPPING ==========
# Female voices for each language
VOICE_MAP = {
    "English": "en-US-JennyNeural",
    "French": "fr-FR-DeniseNeural",
    "Spanish": "es-ES-ElviraNeural"
}

# Script for voice explanation (will be translated on the fly)
EXPLANATION_SCRIPT = {
    "English": "Welcome to the System Health AI Monitor, built by Gesner Deslandes, Engineer‑in‑Chief at GlobalInternet.py. This software simulates real‑time system metrics including CPU, memory, disk usage, and network latency. It automatically detects anomalies and logs alerts. The AI analyst powered by Groq uses Llama 3.1 to provide predictive insights and recommendations. You can adjust the refresh rate, enable auto‑refresh, and run AI analysis at any time. The dashboard shows live trends and alerts. This tool is ideal for platform engineers and software architects to demonstrate observability and AI‑assisted operations.",
    "French": "Bienvenue dans le Moniteur de santé système en temps réel, conçu par Gesner Deslandes, ingénieur en chef chez GlobalInternet.py. Ce logiciel simule des métriques système en temps réel : CPU, mémoire, disque et latence réseau. Il détecte automatiquement les anomalies et enregistre des alertes. L'analyste IA, propulsé par Groq, utilise Llama 3.1 pour fournir des analyses prédictives et des recommandations. Vous pouvez ajuster la fréquence de rafraîchissement, activer le rafraîchissement automatique et lancer l'analyse IA à tout moment. Le tableau de bord montre les tendances en direct et les alertes. Cet outil est idéal pour les ingénieurs plateforme et les architectes logiciels pour démontrer l'observabilité et les opérations assistées par IA.",
    "Spanish": "Bienvenido al Monitor de salud del sistema en tiempo real, construido por Gesner Deslandes, ingeniero jefe de GlobalInternet.py. Este software simula métricas del sistema en tiempo real: CPU, memoria, uso de disco y latencia de red. Detecta automáticamente anomalías y registra alertas. El analista de IA, impulsado por Groq, utiliza Llama 3.1 para proporcionar información predictiva y recomendaciones. Puede ajustar la frecuencia de actualización, habilitar la actualización automática y ejecutar el análisis de IA en cualquier momento. El tablero muestra tendencias en vivo y alertas. Esta herramienta es ideal para ingenieros de plataforma y arquitectos de software para demostrar observabilidad y operaciones asistidas por IA."
}

# ========== SESSION STATE ==========
if "history" not in st.session_state:
    st.session_state.history = []
if "alert_log" not in st.session_state:
    st.session_state.alert_log = []
if "last_ai" not in st.session_state:
    st.session_state.last_ai = None
if "auto_refresh" not in st.session_state:
    st.session_state.auto_refresh = False
if "lang" not in st.session_state:
    st.session_state.lang = "English"

# ========== CUSTOM CSS (LIGHT BLUE THEME) ==========
st.markdown("""
<style>
    .stApp { background-color: #e6f4ff; color: #1a2a3a; }
    [data-testid="stSidebar"] { background-color: #b8d9ff; border-right: 1px solid #7bb3e0; }
    .security-badge { background-color: #d9ebff; border: 1px solid #2c7be5; border-radius: 30px; padding: 8px 15px; text-align: center; color: #0a4c8c; font-weight: bold; font-family: monospace; }
    h1, h2, h3, h4, h5, h6 { color: #0a4c8c; }
    p, li, .stMarkdown { color: #1a2a3a; }
    .stButton>button { background-color: #2c7be5; color: white; border-radius: 25px; }
    .stButton>button:hover { background-color: #1a5bbf; }
    .stMetric { background-color: white; border-radius: 12px; padding: 0.5rem; }
</style>
""", unsafe_allow_html=True)

# ========== GROQ CLIENT ==========
if "GROQ_API_KEY" not in st.secrets:
    st.error("❌ Missing Groq API key. Add `GROQ_API_KEY` to your Streamlit secrets.")
    st.stop()
groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ========== HELPER: GENERATE VOICE (ASYNC) ==========
def generate_voice(lang, text):
    """Generate TTS audio using edge-tts (female voice for language) and return audio bytes."""
    voice = VOICE_MAP.get(lang, "en-US-JennyNeural")
    try:
        # Use asyncio run
        async def _tts():
            comm = edge_tts.Communicate(text, voice)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                tmp_path = tmp.name
            await comm.save(tmp_path)
            with open(tmp_path, "rb") as f:
                audio_bytes = f.read()
            os.unlink(tmp_path)
            return audio_bytes
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        audio_bytes = loop.run_until_complete(_tts())
        loop.close()
        return audio_bytes
    except Exception as e:
        st.error(f"{TEXTS[lang]['explain_error']} {e}")
        return None

# ========== SIMULATE METRICS ==========
def generate_metrics():
    cpu = random.uniform(5, 95)
    memory = random.uniform(20, 90)
    disk = random.uniform(30, 85)
    latency = random.uniform(10, 250)
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
        alert = f"⚠️ High {'CPU' if metrics['cpu']>90 else 'Latency'}: {metrics['cpu'] if metrics['cpu']>90 else metrics['latency']}"
        st.session_state.alert_log.append({"time": metrics["timestamp"], "alert": alert})
        if len(st.session_state.alert_log) > 20:
            st.session_state.alert_log.pop(0)

# ========== AI ANALYSIS (Translated) ==========
def ai_analyze(metrics_df, lang):
    recent = metrics_df.tail(10).to_string()
    if lang == "English":
        prompt = f"""You are a systems reliability engineer. Analyze the following system metrics (CPU%, Memory%, Disk%, Latency ms) and provide:
- Brief anomaly detection
- Recommended action
- Predicted health score (0-100)
Respond in 3-4 short sentences in English.

Metrics:
{recent}
"""
    elif lang == "French":
        prompt = f"""Vous êtes un ingénieur en fiabilité des systèmes. Analysez les métriques suivantes (CPU%, Mémoire%, Disque%, Latence ms) et fournissez :
- Détection brève d'anomalies
- Action recommandée
- Score de santé prédit (0-100)
Répondez en 3-4 phrases courtes en français.

Métriques :
{recent}
"""
    else:  # Spanish
        prompt = f"""Eres un ingeniero de confiabilidad de sistemas. Analiza las siguientes métricas (CPU%, Memoria%, Disco%, Latencia ms) y proporciona:
- Detección breve de anomalías
- Acción recomendada
- Puntuación de salud predicha (0-100)
Responde en 3-4 oraciones cortas en español.

Métricas:
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
        return f"{TEXTS[lang]['ai_unavailable']}: {e}"

# ========== SIDEBAR ==========
with st.sidebar:
    st.title("📊 System Health AI")
    lang = st.selectbox("🌐 Language", ["English", "French", "Spanish"], key="lang_selector")
    if lang != st.session_state.lang:
        st.session_state.lang = lang
        st.rerun()
    texts = TEXTS[st.session_state.lang]
    
    st.markdown("---")
    st.markdown("### 🛡️ Global Security Shield")
    st.markdown(f'<div class="security-badge">{texts["security_badge"]}<br>{texts["security_caption"]}</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**Built by Gesner Deslandes**  \nEngineer‑in‑Chief, GlobalInternet.py")
    st.markdown("📞 (509) 4738 5663")
    st.markdown("✉️ deslandes78@gmail.com")
    st.markdown("---")
    
    # AI Voice Explanation Button
    if st.button(texts["explain_btn"], use_container_width=True):
        with st.spinner(texts["generating_audio"]):
            script = EXPLANATION_SCRIPT[st.session_state.lang]
            audio_bytes = generate_voice(st.session_state.lang, script)
            if audio_bytes:
                st.audio(audio_bytes, format="audio/mp3")
                st.success(texts["explain_playing"])
            else:
                st.error(texts["explain_error"])
    
    st.markdown("---")
    refresh_rate = st.selectbox(texts["refresh_rate"], [1, 2, 5, 10], index=2)
    auto = st.checkbox(texts["auto_refresh"], value=st.session_state.auto_refresh)
    st.session_state.auto_refresh = auto
    if st.button(texts["refresh_now"], use_container_width=True):
        add_metric()
        st.rerun()

# ========== MAIN DASHBOARD ==========
texts = TEXTS[st.session_state.lang]
st.title(texts["title"])
st.caption(texts["caption"])

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
        st.metric(texts["cpu"], f"{latest['cpu']}%", delta=f"{latest['cpu'] - df.iloc[-2]['cpu'] if len(df)>1 else 0:.1f}%" if len(df)>1 else None)
    with col2:
        st.metric(texts["memory"], f"{latest['memory']}%", delta=f"{latest['memory'] - df.iloc[-2]['memory'] if len(df)>1 else 0:.1f}%" if len(df)>1 else None)
    with col3:
        st.metric(texts["disk"], f"{latest['disk']}%")
    with col4:
        st.metric(texts["latency"], f"{latest['latency']} ms", delta=f"{latest['latency'] - df.iloc[-2]['latency'] if len(df)>1 else 0:.1f}" if len(df)>1 else None)

    st.subheader(texts["trends"])
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

    st.subheader(texts["ai_title"])
    col_ai, col_alert = st.columns([2, 1])
    with col_ai:
        if st.button(texts["run_ai"]):
            with st.spinner(texts["ai_thinking"]):
                analysis = ai_analyze(df.reset_index(), st.session_state.lang)
                st.session_state.last_ai = analysis
        if st.session_state.last_ai:
            st.info(st.session_state.last_ai)
    with col_alert:
        st.subheader(texts["alerts_title"])
        if st.session_state.alert_log:
            for alert in st.session_state.alert_log[-5:]:
                st.warning(f"{alert['alert']} at {alert['time'].strftime('%H:%M:%S')}")
        else:
            st.success(texts["no_alerts"])
else:
    st.info("Collecting first metrics...")

if st.session_state.auto_refresh:
    add_metric()
    time.sleep(refresh_rate)
    st.rerun()

st.markdown("---")
st.caption(texts["footer"])
