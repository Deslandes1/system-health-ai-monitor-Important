SYSTEM HEALTH AI MONITOR

Real‑time system observability with AI‑powered anomaly detection and predictive analytics.

Streamlit 1.58.0 | Python 3.10+ | Groq API | MIT License

-------------------------------------------------------------------------------

OVERVIEW

The System Health AI Monitor is a powerful real‑time monitoring dashboard that tracks critical system metrics including CPU usage, memory consumption, disk utilization, and network latency. It automatically detects anomalies, logs alerts, and provides predictive insights powered by Groq's Llama 3.1 AI model.

The app displays detailed system information about your device – device type, brand, model, hostname, operating system, processor, memory, IP addresses, network adapters, and more. A Global Shield API key integration shows your security status at a glance.

-------------------------------------------------------------------------------

FEATURES

- Real‑time metrics for CPU, memory, disk, and latency.
- Switch between Demo mode (simulated data) and Live mode (real system metrics using psutil).
- AI predictive analysis using Groq's Llama 3.1 for anomaly detection and recommendations.
- Detailed system information: device type, brand, model, OS, processor, memory, IPs, MACs, adapters, gateway, DNS, public IP.
- Automatic device type detection (Laptop / Desktop).
- Global Shield integration to display security status via API key.
- AI voice explanation in English, French, and Spanish (female voice).
- Multi‑language support for the entire interface.
- Step‑by‑step local installation instructions in the sidebar.
- Configurable auto‑refresh rate (1, 2, 5, or 10 seconds).
- Real‑time alerts for high CPU or latency.
- Interactive Plotly charts for trend visualization.

-------------------------------------------------------------------------------

LIVE DEMO

You can test the fully functional application at the following link:

https://system-health-ai-monitor-important-9bemdyosmbfmtx4t8wygbv.streamlit.app/

No login required – just open the link and start testing.

-------------------------------------------------------------------------------

INSTALLATION AND LOCAL SETUP

To monitor your own laptop or device, clone and run the app locally.

Step 1 – Clone the repository
git clone https://github.com/Deslandes1/system-health-ai-monitor-Important

Step 2 – Navigate into the folder
cd system-health-ai-monitor-Important

Step 3 – Install the required dependencies
pip install -r requirements.txt

Step 4 – Run the Streamlit app
streamlit run app.py

Step 5 – Open your browser
Visit the local URL shown in the terminal (usually http://localhost:8501).

Step 6 – Switch to Live mode
In the sidebar, select "Live (Real System)" to see your actual laptop metrics.

-------------------------------------------------------------------------------

CONFIGURATION (SECRETS)

Create a .streamlit/secrets.toml file in your project root with the following content:

GROQ_API_KEY = "your-groq-api-key"
GLOBAL_SHIELD_API_KEY = "your-global-shield-api-key"

GROQ_API_KEY is required – get it from Groq Cloud (console.groq.com).
GLOBAL_SHIELD_API_KEY is optional – it displays security status in the sidebar.

The app will still run without the Global Shield key, but the badge will show "Not configured".

-------------------------------------------------------------------------------

DEPENDENCIES

The app uses the following Python packages:

streamlit (>=1.28.0)
pandas (>=2.0.0)
plotly (>=5.0.0)
numpy (>=1.21.0)
groq (>=0.5.0)
edge-tts (>=6.1.9)
psutil (>=5.9.0)
netifaces (>=0.11.0)

Install all dependencies with:

pip install -r requirements.txt

-------------------------------------------------------------------------------

GLOBAL SHIELD INTEGRATION

The app checks for a GLOBAL_SHIELD_API_KEY in your Streamlit secrets. If present, the sidebar displays a green badge:

"Global Shield: Active"

If missing, it shows a red badge:

"Global Shield: Not configured"

-------------------------------------------------------------------------------

AI VOICE EXPLANATION

Click the "AI Voice Explanation" button in the sidebar to hear a female voice describe the entire application in your chosen language (English, French, or Spanish). The voice script includes an overview of the app, explanation of Demo vs. Live mode, system information display, Global Shield integration, pricing, and contact details.

-------------------------------------------------------------------------------

MULTI-LANGUAGE SUPPORT

The app is fully translated into English, Français, and Español. Select your preferred language from the sidebar dropdown.

-------------------------------------------------------------------------------

HOW IT WORKS

Metrics Generation

- Demo Mode – Simulates random system metrics with occasional spikes to demonstrate anomaly detection.
- Live Mode – Uses the psutil library to read real system metrics from your computer.

Anomaly Detection

- Alerts are triggered when:
  - CPU usage exceeds 90%
  - Network latency exceeds 300 ms

AI Analysis

- The app sends the last 10 data points to Groq's Llama 3.1 model.
- The AI responds with:
  - Brief anomaly detection
  - Recommended action
  - Predicted health score (0-100)

System Information

- Uses psutil, platform, socket, netifaces, and system APIs to gather:
  - Device type (Laptop/Desktop)
  - Brand and Model
  - Hostname
  - Operating System
  - Processor and Cores
  - Memory (total, available, used, percentage)
  - IP addresses (all interfaces)
  - MAC addresses
  - Network adapters (status and speed)
  - Default gateway
  - DNS servers
  - Public IP

-------------------------------------------------------------------------------

TECHNOLOGIES USED

- Python 3.10+
- Streamlit – Web interface
- Groq – AI-powered analytics via Llama 3.1
- psutil – Real system metrics
- netifaces – Network gateway detection
- edge-tts – AI voice generation
- Plotly – Interactive charts
- Pandas / NumPy – Data processing

-------------------------------------------------------------------------------

LICENSE

This project is licensed under the MIT License – see the LICENSE file in the repository for details.

-------------------------------------------------------------------------------

ABOUT THE DEVELOPER

This software was built by Gesner Deslandes, Engineer‑in‑Chief at GlobalInternet.py.

We deliver tailored software solutions connecting global markets with local expertise – in healthcare, education, AI, and automation.

Contact and Pricing

Email: deslandes78@gmail.com
Phone / WhatsApp: (509) 4738 5663
Website: https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/
GitHub: https://github.com/Deslandes1

Pricing: Full license starting at 499 USD, including complete source code and setup support.

-------------------------------------------------------------------------------

ACKNOWLEDGEMENTS

- Streamlit – For the amazing web framework
- Groq – For the lightning‑fast AI inference
- psutil – For cross‑platform system monitoring
- netifaces – For network gateway detection

-------------------------------------------------------------------------------

SUPPORT

For bug reports, feature requests, or any questions, please open an issue on GitHub:

https://github.com/Deslandes1/system-health-ai-monitor-Important/issues

We aim to respond within 48 hours.

Built with ❤️ in Haiti by Gesner Deslandes – GlobalInternet.py
