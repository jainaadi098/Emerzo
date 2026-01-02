from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import math
from app.db.database import engine, get_db
from app import models, schemas

# Initialize Database

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

@app.get("/")
def home():
    return {"message": "Emerzo Backend Database is Ready!"}

@app.post("/api/emergency", response_model=schemas.EmergencyResponse)
def trigger_emergency(data: schemas.EmergencyCreate, db: Session = Depends(get_db)):
    hospitals = db.query(models.Hospital).filter(models.Hospital.supports_emergency == True).all()
    if not hospitals:
        raise HTTPException(status_code=404, detail="No hospitals found. (Did you run the seed script?)")

    nearest_hospital = None
    min_distance = float('inf')

    for hospital in hospitals:
        dist = calculate_distance(data.latitude, data.longitude, hospital.latitude, hospital.longitude)
        if dist < min_distance:
            min_distance = dist
            nearest_hospital = hospital

    if not nearest_hospital:
        raise HTTPException(status_code=404, detail="No suitable hospital found.")

    new_request = models.EmergencyRequest(
        latitude=data.latitude, longitude=data.longitude,
        status="Routed", emergency_type=data.emergency_type
    )
    db.add(new_request)
    db.commit()

    return {
        "message": "Emergency Declared!",
        "hospital_name": nearest_hospital.name,
        "contact_number": nearest_hospital.contact_number,
        "distance_km": round(min_distance, 2),
        "status": "Routed"
    }