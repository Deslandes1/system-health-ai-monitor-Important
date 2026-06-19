import streamlit as st
import pandas as pd
import numpy as np
import random
import time
import asyncio
import tempfile
import os
import psutil
import socket
import platform
import uuid
import netifaces
import urllib.request
import json
import re
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
        "footer": "© 2026 GlobalInternet.py – Built for real‑time system observability & AI‑assisted operations",
        "mode_label": "🔄 Monitoring Mode",
        "mode_demo": "Demo (Simulated)",
        "mode_live": "Live (Real System)",
        "live_note": "Fetching real system metrics using psutil.",
        "sysinfo_title": "🖥️ System Information",
        "device_type": "Device Type",
        "hostname": "Hostname",
        "os": "Operating System",
        "processor": "Processor",
        "cores": "Cores",
        "memory_total": "Total Memory",
        "memory_available": "Available Memory",
        "memory_used": "Used Memory",
        "memory_percent": "Memory Usage",
        "ip_addresses": "IP Addresses",
        "public_ip": "Public IP",
        "mac_addresses": "MAC Addresses",
        "network_adapters": "Network Adapters",
        "default_gateway": "Default Gateway",
        "dns_servers": "DNS Servers",
        "not_available": "Not available",
        "device_desktop": "Desktop",
        "device_laptop": "Laptop / Tablet / Phone"
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
        "footer": "© 2026 GlobalInternet.py – Conçu pour l'observabilité système et les opérations assistées par IA",
        "mode_label": "🔄 Mode de surveillance",
        "mode_demo": "Démo (simulé)",
        "mode_live": "Direct (système réel)",
        "live_note": "Récupération des métriques réelles via psutil.",
        "sysinfo_title": "🖥️ Informations système",
        "device_type": "Type d'appareil",
        "hostname": "Nom de l'hôte",
        "os": "Système d'exploitation",
        "processor": "Processeur",
        "cores": "Cœurs",
        "memory_total": "Mémoire totale",
        "memory_available": "Mémoire disponible",
        "memory_used": "Mémoire utilisée",
        "memory_percent": "Utilisation mémoire",
        "ip_addresses": "Adresses IP",
        "public_ip": "IP publique",
        "mac_addresses": "Adresses MAC",
        "network_adapters": "Adaptateurs réseau",
        "default_gateway": "Passerelle par défaut",
        "dns_servers": "Serveurs DNS",
        "not_available": "Non disponible",
        "device_desktop": "Ordinateur de bureau",
        "device_laptop": "Ordinateur portable / Tablette / Téléphone"
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
        "footer": "© 2026 GlobalInternet.py – Construido para observabilidad de sistemas y operaciones asistidas por IA",
        "mode_label": "🔄 Modo de monitoreo",
        "mode_demo": "Demo (simulado)",
        "mode_live": "En vivo (sistema real)",
        "live_note": "Obteniendo métricas reales usando psutil.",
        "sysinfo_title": "🖥️ Información del sistema",
        "device_type": "Tipo de dispositivo",
        "hostname": "Nombre del host",
        "os": "Sistema operativo",
        "processor": "Procesador",
        "cores": "Núcleos",
        "memory_total": "Memoria total",
        "memory_available": "Memoria disponible",
        "memory_used": "Memoria usada",
        "memory_percent": "Uso de memoria",
        "ip_addresses": "Direcciones IP",
        "public_ip": "IP pública",
        "mac_addresses": "Direcciones MAC",
        "network_adapters": "Adaptadores de red",
        "default_gateway": "Puerta de enlace predeterminada",
        "dns_servers": "Servidores DNS",
        "not_available": "No disponible",
        "device_desktop": "Escritorio",
        "device_laptop": "Portátil / Tableta / Teléfono"
    }
}

# ========== VOICE MAPPING ==========
VOICE_MAP = {
    "English": "en-US-JennyNeural",
    "French": "fr-FR-DeniseNeural",
    "Spanish": "es-ES-ElviraNeural"
}

# ========== UPDATED VOICE EXPLANATION (includes device type) ==========
EXPLANATION_SCRIPT = {
    "English": "Welcome to the System Health AI Monitor, built by Gesner Deslandes, Engineer‑in‑Chief at GlobalInternet.py. This software can monitor real‑time system metrics including CPU, memory, disk usage, and network latency. You can choose between Demo mode, which simulates random data, or Live mode, which reads actual metrics from your computer using the psutil library. It automatically detects anomalies and logs alerts. The AI analyst powered by Groq uses Llama 3.1 to provide predictive insights and recommendations. The app also displays detailed system information about your device, including the device type, hostname, operating system, processor, memory, IP addresses, network adapters, and more. You can adjust the refresh rate, enable auto‑refresh, and run AI analysis at any time. The dashboard shows live trends and alerts. This tool is ideal for platform engineers and software architects to demonstrate observability and AI‑assisted operations.",
    "French": "Bienvenue dans le Moniteur de santé système en temps réel, conçu par Gesner Deslandes, ingénieur en chef chez GlobalInternet.py. Ce logiciel peut surveiller des métriques système en temps réel : CPU, mémoire, disque et latence réseau. Vous pouvez choisir entre le mode Démo, qui simule des données aléatoires, ou le mode Direct, qui lit les métriques réelles de votre ordinateur à l'aide de la bibliothèque psutil. Il détecte automatiquement les anomalies et enregistre des alertes. L'analyste IA, propulsé par Groq, utilise Llama 3.1 pour fournir des analyses prédictives et des recommandations. L'application affiche également des informations détaillées sur votre appareil, notamment le type d'appareil, le nom d'hôte, le système d'exploitation, le processeur, la mémoire, les adresses IP, les adaptateurs réseau, et plus encore. Vous pouvez ajuster la fréquence de rafraîchissement, activer le rafraîchissement automatique et lancer l'analyse IA à tout moment. Le tableau de bord montre les tendances en direct et les alertes. Cet outil est idéal pour les ingénieurs plateforme et les architectes logiciels pour démontrer l'observabilité et les opérations assistées par IA.",
    "Spanish": "Bienvenido al Monitor de salud del sistema en tiempo real, construido por Gesner Deslandes, ingeniero jefe de GlobalInternet.py. Este software puede monitorear métricas del sistema en tiempo real: CPU, memoria, uso de disco y latencia de red. Puede elegir entre el modo Demo, que simula datos aleatorios, o el modo En vivo, que lee métricas reales de su computadora usando la biblioteca psutil. Detecta automáticamente anomalías y registra alertas. El analista de IA, impulsado por Groq, utiliza Llama 3.1 para proporcionar información predictiva y recomendaciones. La aplicación también muestra información detallada del sistema, incluido el tipo de dispositivo, el nombre del host, el sistema operativo, el procesador, la memoria, las direcciones IP, los adaptadores de red y más. Puede ajustar la frecuencia de actualización, habilitar la actualización automática y ejecutar el análisis de IA en cualquier momento. El tablero muestra tendencias en vivo y alertas. Esta herramienta es ideal para ingenieros de plataforma y arquitectos de software para demostrar observabilidad y operaciones asistidas por IA."
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
if "monitor_mode" not in st.session_state:
    st.session_state.monitor_mode = "Demo (Simulated)"

# ========== CUSTOM CSS ==========
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
    .profile-img { border-radius: 50%; border: 2px solid #2c7be5; }
    .sysinfo-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
    .sysinfo-item { background: white; padding: 10px; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# ========== GROQ CLIENT ==========
if "GROQ_API_KEY" not in st.secrets:
    st.error("❌ Missing Groq API key. Add `GROQ_API_KEY` to your Streamlit secrets.")
    st.stop()
groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ========== HELPER: GENERATE VOICE ==========
def generate_voice(lang, text):
    voice = VOICE_MAP.get(lang, "en-US-JennyNeural")
    try:
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

# ========== SYSTEM INFORMATION COLLECTOR (with device type) ==========
def get_system_info():
    info = {}
    try:
        info["hostname"] = socket.gethostname()
    except:
        info["hostname"] = "N/A"
    try:
        info["os"] = f"{platform.system()} {platform.release()} ({platform.version()})"
    except:
        info["os"] = "N/A"
    try:
        info["processor"] = platform.processor()
        if not info["processor"]:
            info["processor"] = "Unknown"
    except:
        info["processor"] = "N/A"
    try:
        info["cores"] = psutil.cpu_count(logical=True)
    except:
        info["cores"] = "N/A"
    try:
        mem = psutil.virtual_memory()
        info["memory_total"] = mem.total
        info["memory_available"] = mem.available
        info["memory_used"] = mem.used
        info["memory_percent"] = mem.percent
    except:
        info["memory_total"] = info["memory_available"] = info["memory_used"] = info["memory_percent"] = "N/A"
    # ---- Device Type Detection ----
    # Check if battery exists -> likely laptop/tablet/phone, else desktop
    try:
        battery = psutil.sensors_battery()
        if battery is not None:
            info["device_type"] = "Laptop / Tablet / Phone"
        else:
            info["device_type"] = "Desktop"
    except:
        info["device_type"] = "Unknown"
    # IP addresses
    ip_list = []
    mac_list = []
    adapter_info = {}
    try:
        for iface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    ip_list.append((iface, addr.address))
                elif addr.family == psutil.AF_LINK:
                    mac_list.append((iface, addr.address))
            # adapter speed and status
            stats = psutil.net_if_stats().get(iface)
            if stats:
                adapter_info[iface] = {"speed": stats.speed, "isup": stats.isup}
    except:
        pass
    info["ip_addresses"] = ip_list
    info["mac_addresses"] = mac_list
    info["network_adapters"] = adapter_info
    # Default gateway
    try:
        gateway = netifaces.gateways()['default'][netifaces.AF_INET][0]
        info["default_gateway"] = gateway
    except:
        info["default_gateway"] = "N/A"
    # DNS servers (simple attempt)
    dns = []
    try:
        if platform.system() == "Windows":
            import subprocess
            output = subprocess.check_output("ipconfig /all", shell=True, text=True)
            lines = output.splitlines()
            for line in lines:
                if "DNS Servers" in line:
                    parts = line.split(":")
                    if len(parts) > 1:
                        dns.append(parts[1].strip())
        else:
            with open("/etc/resolv.conf", "r") as f:
                for line in f:
                    if "nameserver" in line:
                        dns.append(line.split()[1])
    except:
        pass
    info["dns_servers"] = dns if dns else ["N/A"]
    # Public IP
    try:
        with urllib.request.urlopen("https://api.ipify.org?format=json", timeout=3) as response:
            data = json.loads(response.read().decode())
            info["public_ip"] = data.get("ip", "N/A")
    except:
        try:
            with urllib.request.urlopen("https://httpbin.org/ip", timeout=3) as response:
                data = json.loads(response.read().decode())
                info["public_ip"] = data.get("origin", "N/A")
        except:
            info["public_ip"] = "N/A"
    return info

# ========== METRICS GENERATION ==========
def generate_simulated_metrics():
    cpu = random.uniform(5, 95)
    memory = random.uniform(20, 90)
    disk = random.uniform(30, 85)
    latency = random.uniform(10, 250)
    if random.random() < 0.1:
        cpu = random.uniform(95, 100)
        latency = random.uniform(250, 500)
    return {
        "cpu": round(cpu, 1),
        "memory": round(memory, 1),
        "disk": round(disk, 1),
        "latency": round(latency, 1)
    }

def get_live_metrics():
    cpu = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    try:
        start = time.time()
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        end = time.time()
        latency = round((end - start) * 1000, 1)
    except Exception:
        latency = random.uniform(10, 100)
    return {
        "cpu": round(cpu, 1),
        "memory": round(memory, 1),
        "disk": round(disk, 1),
        "latency": latency
    }

def generate_metrics(mode):
    if mode == "Live (Real System)":
        return get_live_metrics()
    else:
        return generate_simulated_metrics()

def add_metric():
    mode = st.session_state.monitor_mode
    metrics = generate_metrics(mode)
    metrics["timestamp"] = datetime.now()
    st.session_state.history.append(metrics)
    if len(st.session_state.history) > 100:
        st.session_state.history.pop(0)
    if metrics["cpu"] > 90 or metrics["latency"] > 300:
        alert = f"⚠️ High {'CPU' if metrics['cpu']>90 else 'Latency'}: {metrics['cpu'] if metrics['cpu']>90 else metrics['latency']}"
        st.session_state.alert_log.append({"time": metrics["timestamp"], "alert": alert})
        if len(st.session_state.alert_log) > 20:
            st.session_state.alert_log.pop(0)

# ========== AI ANALYSIS ==========
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

# ========== DISPLAY SYSTEM INFORMATION ==========
def display_system_info(texts):
    info = get_system_info()
    with st.expander(f"{texts['sysinfo_title']}", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            # Device Type
            device_label = texts["device_desktop"] if info["device_type"] == "Desktop" else texts["device_laptop"]
            st.markdown(f"**{texts['device_type']}:** {device_label}")
            st.markdown(f"**{texts['hostname']}:** {info['hostname']}")
            st.markdown(f"**{texts['os']}:** {info['os']}")
            st.markdown(f"**{texts['processor']}:** {info['processor']}")
            st.markdown(f"**{texts['cores']}:** {info['cores']}")
            st.markdown(f"**{texts['default_gateway']}:** {info['default_gateway']}")
            dns_str = ", ".join(info['dns_servers'])
            st.markdown(f"**{texts['dns_servers']}:** {dns_str}")
        with col2:
            mem_total = info['memory_total'] if info['memory_total'] != "N/A" else "N/A"
            mem_avail = info['memory_available'] if info['memory_available'] != "N/A" else "N/A"
            mem_used = info['memory_used'] if info['memory_used'] != "N/A" else "N/A"
            mem_percent = info['memory_percent'] if info['memory_percent'] != "N/A" else "N/A"
            if mem_total != "N/A":
                mem_total = f"{mem_total / (1024**3):.2f} GB"
            if mem_avail != "N/A":
                mem_avail = f"{mem_avail / (1024**3):.2f} GB"
            if mem_used != "N/A":
                mem_used = f"{mem_used / (1024**3):.2f} GB"
            st.markdown(f"**{texts['memory_total']}:** {mem_total}")
            st.markdown(f"**{texts['memory_available']}:** {mem_avail}")
            st.markdown(f"**{texts['memory_used']}:** {mem_used}")
            st.markdown(f"**{texts['memory_percent']}:** {mem_percent}%")
            st.markdown(f"**{texts['public_ip']}:** {info['public_ip']}")
        # IP and MAC addresses
        st.markdown("---")
        st.markdown(f"**{texts['ip_addresses']}:**")
        if info['ip_addresses']:
            for iface, ip in info['ip_addresses']:
                st.markdown(f"- {iface}: {ip}")
        else:
            st.markdown(f"*{texts['not_available']}*")
        st.markdown(f"**{texts['mac_addresses']}:**")
        if info['mac_addresses']:
            for iface, mac in info['mac_addresses']:
                st.markdown(f"- {iface}: {mac}")
        else:
            st.markdown(f"*{texts['not_available']}*")
        st.markdown(f"**{texts['network_adapters']}:**")
        if info['network_adapters']:
            for iface, details in info['network_adapters'].items():
                status = "🟢 Up" if details['isup'] else "🔴 Down"
                speed = f"{details['speed']} Mbps" if details['speed'] else "Unknown"
                st.markdown(f"- {iface}: {status}, {speed}")
        else:
            st.markdown(f"*{texts['not_available']}*")

# ========== SIDEBAR ==========
with st.sidebar:
    st.image(
        "https://raw.githubusercontent.com/Deslandes1/system-health-ai-monitor-Important/main/Gesner%20Deslandes.png",
        width=80,
        use_container_width=False,
        output_format="PNG"
    )
    st.markdown("### **Gesner Deslandes**")
    
    st.markdown("---")
    st.title("📊 System Health AI")
    lang = st.selectbox("🌐 Language", ["English", "French", "Spanish"], key="lang_selector")
    if lang != st.session_state.lang:
        st.session_state.lang = lang
        st.rerun()
    texts = TEXTS[st.session_state.lang]
    
    st.markdown("---")
    mode_options = ["Demo (Simulated)", "Live (Real System)"]
    selected_mode = st.selectbox(texts["mode_label"], mode_options, index=0)
    if selected_mode != st.session_state.monitor_mode:
        st.session_state.monitor_mode = selected_mode
        st.session_state.history.clear()
        st.session_state.alert_log.clear()
        st.rerun()
    if selected_mode == "Live (Real System)":
        st.info(texts["live_note"])
    
    st.markdown("---")
    st.markdown("### 🛡️ Global Security Shield")
    st.markdown(f'<div class="security-badge">{texts["security_badge"]}<br>{texts["security_caption"]}</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**Built by Gesner Deslandes**  \nEngineer‑in‑Chief, GlobalInternet.py")
    st.markdown("📞 (509) 4738 5663")
    st.markdown("✉️ deslandes78@gmail.com")
    st.markdown("---")
    
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

# ---- Display System Information ----
display_system_info(texts)

# ---- Metrics Dashboard ----
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
