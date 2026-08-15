# IoT Real-Time Telemetry & Monitoring Dashboard

This repository contains the firmware and python-based dashboard applications for real-time monitoring of environment and telemetry data collected via an ESP32 microcontroller.

## Overview
- **Microcontroller:** ESP32
- **Sensors:** DHT11 (Temperature & Humidity), LDR (Light Intensity), HC-SR04 (Ultrasonic Distance)
- **Protocol:** MQTT / WebSockets
- **Dashboard Framework:** Dash & Plotly (Python)

## Directory Structure
```text
iot-telemetry-dashboard/
│
├── firmware/
│   └── esp32_telemetry.ino
│
├── dashboard/
│   ├── realtime_dashboard.py
│   └── advanced_dashboard.py
│
├── assets/
│   ├── dashboard_preview.png
│   └── terminal_logs.png
│
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup & Running
1. **Firmware:** Flash `firmware/esp32_telemetry.ino` to the ESP32 via Arduino IDE after updating Wi-Fi credentials.
2. **Dependencies:** Install required Python modules:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run Dashboard:**
   ```bash
   python dashboard/advanced_dashboard.py
   ```
