# 🛡️ ddos_tool_2025

**`ddos_tool_2025`** is an **open-source DDoS stress-testing framework** built for **ethical hacking** and **authorized infrastructure testing** only.  
It provides **multi-layer attacks (L3/L4 & L7)**, **Cloudflare bypass techniques**, and **reflection-based amplification attacks**, giving security researchers a powerful tool for evaluating network resilience.

---

## 🚀 Supported Attacks
- 🔹 **UDP Flood** – Stress test network capacity with high-volume UDP packets.  
- 🔹 **SYN Flood (TCP)** – Exploit TCP handshake to overload server resources.  
- 🔹 **HTTP Flood** – Layer 7 attack leveraging high-rate HTTP requests.  
- 🔹 **Slowloris Attack** – Keeps connections open to exhaust server thread limits.  
- 🔹 **RUDY Attack** – Sends slow, long POST requests for resource exhaustion.  
- 🔹 **NTP Reflection Attack** – Amplified DDoS using vulnerable NTP servers.  
- 🔹 **HTTP Flood (Bypass Cloudflare)** – Evades certain cloud-based protection layers.  
- 🔹 **Layer7 HTTP/1.1 Flood Attack** – High-impact HTTP/1.1 floods.  
- 🔹 **Layer7 HTTP/2 Flood Attack** – Targets HTTP/2 protocols for advanced stress tests.  
- 🔹 **Layer7 WebSocket Flood Attack** – Overwhelms WebSocket connections.

---

## ✨ Features
- ⚡ **Advanced Layer 7 techniques** (HTTP/1.1, HTTP/2, WebSocket).  
- 🔒 **Cloudflare Bypass Methods** built-in.  
- 📈 **Reflection Amplification Attacks** (e.g., NTP).  
- 🖥 **User-friendly CLI** interface.  
- 📊 **Logging & Response Analysis** for result evaluation.  

---

## ⚠️ Legal Disclaimer
> **This tool is intended for educational purposes and authorized stress testing only.**  
> **Any unauthorized or malicious use is strictly prohibited and solely the user’s responsibility.**  

---

## 🛠 Tech Stack
- **Python 3.9+**  
- Lightweight, fast, and modular attack engine

---

## 📥 Installation
```bash
# Clone repository
git clone https://github.com/infocyn/ddos-2025.git

# Navigate into the project folder
cd ddos-2025
# Install dependencies
pip install -r requirements.txt

python main.py

[1] UDP Flood
[2] SYN Flood (TCP)
[3] HTTP Flood
[4] Slowloris Attack
[5] RUDY Attack
[6] NTP Reflection Attack
[7] HTTP Flood (Bypass Cloudflare)
[8] Layer7 HTTP/1.1 Flood Attack
[9] Layer7 HTTP/2 Flood Attack
[10] Layer7 WebSocket Flood Attack
[0] Exit

# Select: 3 (HTTP Flood)
# Target: https://example.com
# Connections: 500
# Duration (seconds): 60





