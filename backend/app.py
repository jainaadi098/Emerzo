from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import httpx
import os

from database import SessionLocal
from models import Hospital
from schemas import Location, HospitalOut

ORS_API_KEY = os.getenv("ORS_API_KEY")
ORS_BASE = "https://api.openrouteservice.org"

app = FastAPI(title="Emerzo Emergency API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/emergency/options", response_model=list[HospitalOut])
async def emergency_options(patient: Location, db: Session = Depends(get_db)):
    hospitals = db.query(Hospital).filter(Hospital.emergency == 1).all()

    if not hospitals:
        raise HTTPException(404, "No emergency hospitals found")

    locations = (
        [[patient.lon, patient.lat]] +
        [[h.lon, h.lat] for h in hospitals]
    )

    payload = {
        "locations": locations,
        "sources": [0],
        "destinations": list(range(1, len(locations))),
        "metrics": ["duration"]
    }

    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.post(
            f"{ORS_BASE}/v2/matrix/driving-car",
            json=payload,
            headers={
                "Authorization": ORS_API_KEY,
                "Content-Type": "application/json"
            }
        )

    durations = r.json()["durations"][0]

    ranked = [{
        "id": h.id,
        "name": h.name,
        "lat": h.lat,
        "lon": h.lon,
        "phone": h.phone,
        "eta_minutes": round(d / 60)
    } for h, d in zip(hospitals, durations)]

    return sorted(ranked, key=lambda x: x["eta_minutes"])[:3]
