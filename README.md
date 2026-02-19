# 🛰️ Bellatrix Orbita

**AI-powered orbital risk intelligence platform** for satellite tracking, collision analysis, and trajectory visualization.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)

---

## 🌟 Features

- **� Real-time Satellite Tracking** — Monitor 27,000+ objects in orbit using NORAD TLE data
- **🗺️ Interactive 2D/3D Visualization** — Ground tracks on world map + Three.js orbital paths
- **🤖 AI Risk Forecasting** — Neural network-based collision probability analysis
- **📊 Telemetry Dashboard** — Live altitude, velocity, inclination, and orbital parameters
- **🌍 Multi-language Support** — Full English and Russian localization
- **⚠️ Collision Alerts** — Automatic warnings for high-risk conjunctions

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.9+**
- **pip** (Python package manager)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/bellatrix-orbita.git
   cd bellatrix-orbita
   ```

2. **Install dependencies:**
   ```bash
   pip install -r backend/requirements.txt
   ```

3. **Launch the platform:**
   ```bash
   ./start_bellatrix.sh
   ```

4. **Open in browser:**
   ```
   http://localhost:8080
   ```

The script automatically starts:
- **Backend API** on port `8000` (FastAPI)
- **Frontend** on port `8080` (HTTP server)

---

## 📂 Project Structure

```
bellatrix-orbita/
├── backend/
│   ├── main.py                 # FastAPI server & API routes
│   ├── celestial_engine.py     # Orbital mechanics & propagation (SGP4)
│   ├── analytics_engine.py     # AI risk analysis & forecasting
│   └── requirements.txt        # Python dependencies
├── frontend/
│   ├── index.html              # React app (embedded JS)
│   └── style.css               # UI styling
├── start_bellatrix.sh          # Auto-start script
├── LICENSE                     # MIT License
└── README.md                   # This file
```

---

## 🛠️ Technology Stack

### Backend
- **FastAPI** — High-performance async API framework
- **SGP4** — Satellite orbit propagation (NORAD algorithms)
- **Uvicorn** — ASGI server

### Frontend
- **React** — Component-based UI
- **Three.js** — 3D orbital visualization
- **Vanilla CSS** — Custom styling with glassmorphism effects

### Data Sources
- **NORAD** — Two-Line Element (TLE) sets
- **CelesTrak** — Satellite catalog API
- **NASA/SpaceX** — Public orbital data

---

## 📖 Usage Guide

### 1. Search & Track Satellites
Navigate to the **Calculator** tab and search by:
- **NORAD ID** (e.g., `25544` for ISS)
- **Satellite Name** (e.g., "Starlink")

### 2. Analyze Risk
Select a satellite to view:
- Real-time telemetry (altitude, velocity, inclination)
- Collision probability
- AI stability forecasts

### 3. Visualize Orbits
Click the **Map** button to see:
- Current position on Earth
- 2D ground track (dotted line)
- 3D orbital path (point cloud)

### 4. AI Forecasting
Go to **AI Forecast** tab for:
- 7-day risk trend analysis
- Neural network stability predictions
- Global sector readiness statistics

---

## 🔧 Development

### Running in Development Mode

**Backend only:**
```bash
cd backend
uvicorn main:app --reload --port 8000
```

**Frontend only:**
```bash
cd frontend
python3 -m http.server 8080
```

### Modifying the Code
- **UI changes:** Edit `frontend/index.html` or `frontend/style.css`
- **API logic:** Edit `backend/main.py`
- **Orbital calculations:** Edit `backend/celestial_engine.py`
- **AI analytics:** Edit `backend/analytics_engine.py`

---

## � API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/satellites` | GET | List all tracked satellites |
| `/api/satellite/{id}/details` | GET | Get satellite telemetry |
| `/api/propagate/{id}` | GET | Calculate future positions |
| `/api/analytics/{id}` | GET | AI risk analysis |
| `/api/stats` | GET | Global statistics |
| `/api/search?q={query}` | GET | Search satellites by name/ID |

---

## 🌐 Localization

The platform supports:
- 🇬🇧 **English** (default)
- 🇷🇺 **Russian** (полная локализация)

Switch languages using the **EN/RU** toggle in the navigation bar.

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

### Third-Party Data Attribution
Satellite orbital data (TLE) is provided by:
- NORAD (North American Aerospace Defense Command)
- CelesTrak ([celestrak.org](https://celestrak.org))
- NASA & SpaceX

All TLE data is in the public domain and used in accordance with respective data policies.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 🐛 Known Issues

- **Chrome requirement:** The `open_browser_url` tool requires Chrome for automated testing
- **CORS:** Ensure backend and frontend run on specified ports to avoid cross-origin issues

---

## 📧 Contact

**Project Maintainer:** Bellatrix Orbita Team  
**Repository:** [github.com/YOUR_USERNAME/bellatrix-orbita](https://github.com/YOUR_USERNAME/bellatrix-orbita)

---

## 🙏 Acknowledgments

- **CelesTrak** for providing free satellite tracking data
- **NORAD** for TLE orbital elements
- **Three.js** community for 3D visualization tools
- **FastAPI** team for the excellent framework

---

**⭐ If you find this project useful, please consider giving it a star!**
# bellatrix
# bellatrix-orbita
