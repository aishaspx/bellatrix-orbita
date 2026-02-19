from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import os
import io
import csv
import datetime
import logging

import os
import sys
sys.path.append(os.path.dirname(__file__))

from celestial_engine import router as celestial_router
import analytics_engine

# --- Logging ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)

# --- Rate Limiter ---
limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])

app = FastAPI(
    title="Bellatrix Orbital Risk API",
    description="AI-powered satellite tracking and orbital risk analysis platform.",
    version="1.0.0"
)

# --- Rate Limit Error Handler ---
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# --- Global Exception Handler ---
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error on {request.url}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc), "path": str(request.url)}
    )

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(celestial_router, prefix="/api")

# --- Health Endpoint ---
@app.get("/api/health")
async def health_check():
    """Uptime monitoring endpoint."""
    return {
        "status": "ok",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "version": "1.0.0",
        "service": "Bellatrix Orbital Risk API"
    }

# --- Analytics Endpoints ---
@app.get("/api/analytics/{norad_id}")
@limiter.limit("30/minute")
async def get_sat_analytics(request: Request, norad_id: str, days: int = 7):
    return analytics_engine.generate_risk_trend(norad_id, days)

@app.get("/api/stats")
@limiter.limit("30/minute")
async def get_global_stats(request: Request):
    return analytics_engine.get_global_stats()

# --- CSV Export ---
@app.get("/api/export/csv/{norad_id}")
@limiter.limit("10/minute")
async def export_csv(request: Request, norad_id: str):
    """Export satellite telemetry as a downloadable CSV file."""
    from celestial_engine import get_tle
    from sgp4.api import Satrec, jday
    import numpy as np

    tle_data = get_tle(norad_id)
    if not tle_data:
        return JSONResponse(status_code=404, content={"error": "Satellite not found"})

    name, line1, line2 = tle_data
    satellite = Satrec.twoline2rv(line1, line2)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["timestamp", "latitude", "longitude", "altitude_km", "velocity_kms"])

    now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
    for i in range(0, 90, 2):  # 90 minutes, every 2 min
        t = now + datetime.timedelta(minutes=i)
        jd, fr = jday(t.year, t.month, t.day, t.hour, t.minute, t.second)
        e, r, v = satellite.sgp4(jd, fr)
        if e == 0:
            r_arr = np.array(r)
            v_arr = np.array(v)
            r_mag = np.linalg.norm(r_arr)
            lat = round(np.arcsin(r_arr[2] / r_mag) * 180 / np.pi, 4)
            lon = (np.arctan2(r_arr[1], r_arr[0]) * 180 / np.pi) - (t.hour * 15 + t.minute * 0.25)
            lon = round((lon + 180) % 360 - 180, 4)
            alt = round(r_mag - 6371.0, 2)
            vel = round(np.linalg.norm(v_arr), 4)
            writer.writerow([t.isoformat(), lat, lon, alt, vel])

    output.seek(0)
    filename = f"bellatrix_{name.replace(' ', '_')}_{norad_id}.csv"
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

# --- PDF Export ---
@app.get("/api/export/pdf/{norad_id}")
@limiter.limit("5/minute")
async def export_pdf(request: Request, norad_id: str):
    """Export satellite risk report as a downloadable PDF."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet
    except ImportError:
        return JSONResponse(status_code=503, content={"error": "PDF export not available. Install reportlab."})

    from celestial_engine import get_tle, calculate_orbital_elements
    from sgp4.api import Satrec, jday
    import numpy as np

    tle_data = get_tle(norad_id)
    if not tle_data:
        return JSONResponse(status_code=404, content={"error": "Satellite not found"})

    name, line1, line2 = tle_data
    satellite = Satrec.twoline2rv(line1, line2)
    now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
    jd, fr = jday(now.year, now.month, now.day, now.hour, now.minute, now.second)
    e, r, v = satellite.sgp4(jd, fr)

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("🛰️ Bellatrix Orbital Risk Report", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Satellite: <b>{name}</b> (NORAD ID: {norad_id})", styles["Normal"]))
    story.append(Paragraph(f"Generated: {now.strftime('%Y-%m-%d %H:%M UTC')}", styles["Normal"]))
    story.append(Spacer(1, 20))

    if e == 0:
        r_arr = np.array(r)
        v_arr = np.array(v)
        alt = round(np.linalg.norm(r_arr) - 6371.0, 1)
        vel = round(np.linalg.norm(v_arr), 2)
        elements = calculate_orbital_elements(satellite)

        data = [
            ["Parameter", "Value"],
            ["Altitude", f"{alt} km"],
            ["Velocity", f"{vel} km/s"],
            ["Period", f"{elements['period_min']} min"],
            ["Inclination", f"{elements['inclination_deg']}°"],
            ["TLE Line 1", line1],
            ["TLE Line 2", line2],
        ]
        table = Table(data, colWidths=[150, 320])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0a0a1a")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0f4ff")]),
        ]))
        story.append(table)

    story.append(Spacer(1, 20))
    story.append(Paragraph("Data source: CelesTrak / NORAD. © 2026 Bellatrix Orbita Project.", styles["Normal"]))

    doc.build(story)
    buf.seek(0)
    filename = f"bellatrix_report_{norad_id}.pdf"
    return StreamingResponse(
        buf,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@app.get("/")
def read_root():
    return {"message": "Bellatrix Orbital Risk Platform Active", "docs": "/docs", "health": "/api/health"}
