# ⚡ FumeGuard OS: Proactive AI Ventilation

An industrial-grade, AI-driven proactive ventilation system designed to predict and neutralize atmospheric hazards before they reach toxic levels. Built for hardware hackathons.

## 📸 Project Showcase
<img width="1280" height="1038" alt="prototype" src="https://github.com/user-attachments/assets/7a6b25ec-aa02-4a29-b888-41b764beed45" />


## 🛠️ System Architecture
This project bridges edge computing, cloud telemetry, and a Quad-Core Machine Learning engine.

* **Hardware (The Edge):** An ESP32 microcontroller processes raw analog data from MQ-135 (Air Quality), MQ-2 (Smoke), and DHT11 (Temperature) sensors.
* **Networking (MQTT Cloud Telemetry):** Telemetry is packaged as lightweight JSON and streamed live via a custom HiveMQ Cloud MQTT broker. Utilizing MQTT's publish/subscribe protocol ensures near-zero latency, minimal bandwidth usage, and robust, decoupled communication between the edge sensors and the AI backend.
* **AI Engine (The Brain):** A Python backend processes the data using Scikit-Learn.
* **Dashboard (The UI):** A high-refresh Streamlit web application with Plotly visualizations.

## 🧠 The Quad-Core AI Engine
Instead of relying on hardcoded safety thresholds, FumeGuard utilizes four concurrent machine learning models:
1. **Electronic Nose (Random Forest Classifier):** Classifies the specific threat as either a "Smoke Profile" or "Toxic Chemical Vapor."
2. **Rupture Detection (Isolation Forest):** Unsupervised anomaly detection that instantly flags sudden, unnatural data spikes (like a pipe bursting).
3. **Proactive Forecasting (Linear Regression):** Predicts the exact trajectory of the gas leak 5 steps into the future to spool up exhaust fans early.
4. **Predictive Maintenance (Statistical Variance):** Analyzes sensor noise during clean air cycles to calculate hardware health and degradation.

## 🔌 Hardware Wiring Guide (ESP32)
* **MQ-135 (Air Quality):** Connected to ESP32 Pin 34 (via 10k/20k Voltage Divider)
* **MQ-2 (Combustibles):** Connected to ESP32 Pin 35 (via 10k/20k Voltage Divider)
* **DHT11 (Temperature):** Connected to ESP32 Pin 32
* **Exhaust Fan (via MOSFET Module):** Connected to ESP32 Pin 26 (PWM Output)
* **Power:** 5V (VIN) / GND

### Circuit Schematic
<img width="1600" height="1512" alt="circuit-diagram" src="https://github.com/user-attachments/assets/0ae876c1-f7c8-4911-b27b-070fea6c62ef" />


## 🚀 How to Run Locally
1. Upload the Arduino `.ino` file to an ESP32 and input your WiFi/HiveMQ credentials.
2. Install Python dependencies: `pip install paho-mqtt scikit-learn pandas plotly streamlit`
3. Start the AI Core: `python ai_engine.py`
4. Launch the Dashboard: `python -m streamlit run dashboard.py`

---
## 👨‍💻 Project Developer
* **Manoj Reddy** - B.Tech Mechatronics Engineering, REVA University
