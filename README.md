# 🇰🇪 KenyaNet AI: Network Traffic Optimizer
> **AI-Driven Bandwidth Rebalancing for High-Load Telecommunications Grids.**

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python: 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)
![Status: Beta](https://img.shields.io/badge/Status-Beta-green.svg)

## 📖 Overview
KenyaNet AI is an optimization framework designed to bridge the gap between physical infrastructure limits and the surging data demands in Kenya's urban hubs. By integrating **Real-Time Traffic Analysis** with **Predictive AI Modeling**, the system mitigates congestion without requiring immediate hardware upgrades.

### ⚡ The Problem
In many developing grids, data spikes (M-Pesa surges, peak streaming hours) lead to high latency and "choked" nodes. Standard expansion is expensive and slow.

### 🤖 The Solution
Our framework uses a **Random Forest Regressor** to predict congestion events 15 minutes before they occur, allowing for dynamic packet-level prioritization and rerouting.

---

## 🛠️ Technical Stack
- **Core Engine:** Python 3.11
- **AI/ML:** Scikit-Learn (Congestion Prediction), Pandas (Data Processing)
- **Monitoring:** Scapy (Packet Sniffing simulation)
- **UI/UX:** Streamlit with Glassmorphism CSS & Folium (GIS Mapping)
- **DevOps:** Docker (Containerized for Cloud Deployment)

---

## 📐 Engineering Logic
The optimization follows the **Shannon-Hartley Theorem**:
$$C = B \log_2(1 + S/N)$$
Where our AI maximizes the **Channel Capacity (C)** by dynamically managing the **Signal-to-Noise ratio (S/N)** through intelligent bandwidth allocation.

---

## 🚀 Getting Started
### 1. Run via Docker (Recommended)
```bash
docker build -t kenyanet-optimizer .
docker run -p 8501:8501 kenyanet-optimizer
