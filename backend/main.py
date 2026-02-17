from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from celestial_engine import router as celestial_router
import analytics_engine
app = FastAPI(title="Bellatrix Orbital Risk API")

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(celestial_router, prefix="/api")

# --- Analytics Endpoints ---
@app.get("/api/analytics/{norad_id}")
async def get_sat_analytics(norad_id: str, days: int = 7):
    return analytics_engine.generate_risk_trend(norad_id, days)

@app.get("/api/stats")
async def get_global_stats():
    return analytics_engine.get_global_stats()

@app.get("/")
def read_root():
    return {"message": "Bellatrix Orbital Risk Platform Active"}
