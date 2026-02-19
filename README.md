# 🛰️ Bellatrix Orbita

**Bellatrix Orbita** is a professional-grade, AI-powered orbital risk intelligence platform. It bridges the gap between raw NORAD tracking data and actionable orbital safety analytics, providing real-time visualization and collision risk assessment for over 27,000 objects in Earth's orbit.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)

---

## 🇷🇺 Описание на русском языке
**Bellatrix Orbita** — это аналитическая платформа для мониторинга орбитальных рисков. Проект объединяет данные слежения NORAD с алгоритмами машинного обучения для прогнозирования вероятности столкновений и визуализации траекторий спутников в реальном времени.

**Основные возможности:**
- **SGP4 Прогнозирование:** Точный расчет положения спутников на основе орбитальных элементов.
- **AI Аналитика Рисков:** Оценка вероятности столкновений на основе сближений и устойчивости орбиты.
- **Интерактивная 3D Визуализация:** Отображение пути спутника на 3D глобусе и 2D карте.
- **Экспорт Отчетов:** Загрузка телеметрии в CSV и PDF отчетов о рисках.
- **Надежность:** Кэширование данных и защита от сбоев API.

---

## 🧠 How It Works (Core Logic)

### 1. Orbital Mechanics (SGP4 Engine)
The system uses the **Simplified General Perturbations (SGP4)** model to propagate satellite positions. 
- **Data Input:** Raw Two-Line Element (TLE) sets from CelesTrak/NORAD.
- **Calculation:** The `celestial_engine.py` converts TLEs into TEME (True Equator Mean Equinox) coordinates, which are then transformed into Geodetic (Latitude, Longitude, Altitude) and ECEF (Earth-Centered, Earth-Fixed) frames for visualization.
- **Propagation:** The platform can propagate an orbit 90-180 minutes into the future to generate the high-visibility "3D Trajectory" points.

### 2. AI Risk Assessment
Collision risk is NOT just distance-based. Our **Analytics Engine** uses a multi-factor heuristic:
- **Proximity Analysis:** Calculates the "Close Approach" distance using future propagation steps.
- **Velocity Differential:** High-speed intersections in Low Earth Orbit (LEO) increase the risk score exponentially.
- **Stability Index:** An AI-generated metric (0-100%) that evaluates the consistency of the satellite's orbital parameters over time.
- **Trend Analysis:** Generates a 7-day risk trend using time-series forecasting to predict future instabilities.

### 3. Reliability & Resilience (The "Phase 20" Upgrades)
- **TLE Disk Cache:** If the external CelesTrak API goes down, Bellatrix reverts to `tle_cache.json` (a disk-based fallback), ensuring 99.9% uptime.
- **Retry Logic:** Implements exponential backoff (3 attempts: 1s → 2s → 4s) for all external network requests.
- **Rate Limiting:** Protects the server from DDoS or heavy scraping using `slowapi` (default 60 requests/minute per IP).

---

## 🛠️ Technology Stack

### Backend (The Brain)
- **FastAPI:** High-speed asynchronous Python framework.
- **SGP4 & Skyfield:** Industrial-standard libraries for orbital physics.
- **ReportLab:** Dynamically generates PDF risk reports.
- **SlowAPI:** Security and rate control.

### Frontend (The HUD)
- **React (CDN):** Component-based architecture for the glassmorphism UI.
- **Three.js:** Renders the 3D Earth, Atmosphere glow, and Satellite models.
- **CSS3:** Advanced dark-mode aesthetics with neon glowing accents.

---

## 📂 Architecture

```bash
bellatrix-orbita/
├── backend/
│   ├── main.py             # API Router, Rate Limiting, & PDF/CSV Export
│   ├── celestial_engine.py # TLE Fetching, SGP4 Propagation, Caching
│   ├── analytics_engine.py # AI Risk Heuristics & Global Stats
│   ├── test_backend.py     # 20+ Unit Tests (High Coverage)
│   └── requirements.txt    # dependencies (fastapi, sgp4, reportlab, etc.)
├── frontend/
│   ├── index.html          # SPA Entry Point & Translation Engine
│   └── style.css           # Mobile-responsive styles (3 Breakpoints)
└── start_bellatrix.sh      # One-click startup script (macOS/Linux)
```

---

## 🚀 Installation & Setup

1. **Clone & Enter:**
   ```bash
   git clone https://github.com/aishaspx/bellatrix-orbita.git
   cd bellatrix-orbita
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r backend/requirements.txt
   ```

3. **Run Locally:**
   ```bash
   ./start_bellatrix.sh
   ```

4. **Run Tests (Verification):**
   ```bash
   cd backend && python3 -m pytest test_backend.py -v
   ```

---

## 📈 Roadmap
- [x] **v1.0**: Core SGP4 Engine & 3D Visualization.
- [x] **v1.1**: Reliability Update (Cache, Rate Limiting, PDF Export).
- [ ] **v1.2**: User Authentication & Saved Satellite Constellations.
- [ ] **v1.3**: Real-time Socket.io updates for telemetry.

---

## 📜 License
Licensed under the [MIT License](LICENSE).

**Data Attribution:** Data provided by NASA, ESA, SpaceX, CelesTrak, and NORAD.

---
**⭐ If you find Bellatrix useful, please consider giving it a star on GitHub!**
