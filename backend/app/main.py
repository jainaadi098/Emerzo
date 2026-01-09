from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import math
import requests #  API call 
import time
import os  
from dotenv import load_dotenv

load_dotenv()

#  folders se import kiya
from . import models, schemas
from ...database.database import engine, get_db

# Tables banayi h
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# API 
ORS_API_KEY =os.getenv("ORS_API_KEY")


# SETTINGS

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#  DISTANCE ENGINE (Hybrid: API + Math Backup )


# 1. Offline Math Formula (Backup Plan)
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0 # Earth radius in Km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# 2. Smart Function (Pehle API, phir Maths)
def get_best_distance(lat1, lon1, lat2, lon2):
    # Agar nhi kam kiya toh maths formula
    if not ORS_API_KEY:
        print(" No API Key found, using Offline Math.")
        return haversine_distance(lat1, lon1, lat2, lon2)

    try:
        # API call kara (Driving Car profile)
        url = f"https://api.openrouteservice.org/v2/directions/driving-car?start={lon1},{lat1}&end={lon2},{lat2}"
        headers = {'Authorization': ORS_API_KEY}
        
        response = requests.get(url, headers=headers, timeout=3) # 3 sec timeout
        
        if response.status_code == 200:
            data = response.json()
            # Distance meters ko km mein convert kiya
            dist_meters = data['features'][0]['properties']['segments'][0]['distance']
            return dist_meters / 1000.0
        else:
            print(f" API Error {response.status_code}: Switching to Offline Math...")
            return haversine_distance(lat1, lon1, lat2, lon2)
            
    except Exception as e:
        print(f" Connection Failed ({e}): Switching to Offline Math...")
        return haversine_distance(lat1, lon1, lat2, lon2)

# main.py mein 'app = FastAPI()' ke neeche yeh jod dein:

@app.get("/")
def read_root():
    return {"message": " Emerzo Backend is Ready! "}


# ---------------------------------------------------------
#  API 1: TRIGGER EMERGENCY
# ---------------------------------------------------------

@app.post("/api/emergency", response_model=schemas.EmergencyResponse)
def trigger_emergency(request: schemas.EmergencyCreate, db: Session = Depends(get_db)):
    print(f" Emergency Request: {request.latitude}, {request.longitude}")

    # Sabse Paas Wala Hospital Dhoondo
    
    hospitals = db.query(models.Hospital).filter(models.Hospital.supports_emergency == True).all()
    
    if not hospitals:
        raise HTTPException(status_code=404, detail="No hospitals found")

    nearest_hospital = None
    min_dist = float("inf")

    # Optimization: Pehle Math se top 3 dhoondo, phir unka Real Road Distance check karo
    
    
    for hospital in hospitals:
        # Yahan ab Smart Function use hoga 
        dist = get_best_distance(request.latitude, request.longitude, hospital.latitude, hospital.longitude)
        
        if dist < min_dist:
            min_dist = dist
            nearest_hospital = hospital

    if not nearest_hospital:
        raise HTTPException(status_code=404, detail="No suitable hospital found")

    # Save to DB
    new_request = models.EmergencyRequest(
        latitude=request.latitude,
        longitude=request.longitude,
        emergency_type=request.emergency_type,
        status="Pending",
        hospital_id=nearest_hospital.id
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    # Notification
    new_notification = models.HospitalNotification(
        request_id=new_request.request_id,
        hospital_id=nearest_hospital.id,
        status="Pending"
    )
    db.add(new_notification)
    db.commit()

    return {
        "message": "Emergency Dispatched!",
        "hospital_name": nearest_hospital.name,
        "distance_km": round(min_dist, 2),
        "status": "Pending",
        "request_id": new_request.request_id,
        "hospital_lat": nearest_hospital.latitude,
        "hospital_lng": nearest_hospital.longitude
    }

# ---------------------------------------------------------
#  API 2: APPROVE REQUEST
# ---------------------------------------------------------
@app.put("/api/emergency/{request_id}/approve")
def approve_emergency(request_id: int, db: Session = Depends(get_db)):
    request = db.query(models.EmergencyRequest).filter(models.EmergencyRequest.request_id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    last_notification = db.query(models.HospitalNotification)\
        .filter(models.HospitalNotification.request_id == request_id)\
        .order_by(models.HospitalNotification.id.desc())\
        .first()

    if last_notification:
        last_notification.status = "Accepted"

    request.status = "Ambulance Dispatched"
    db.commit()

    return {"message": "Request Approved! Ambulance is on the way.", "status": "Ambulance Dispatched"}

# ---------------------------------------------------------
#  API 3: REJECT & RE-ROUTE
# ---------------------------------------------------------
@app.post("/api/emergency/{request_id}/reject")
def reject_and_reroute(request_id: int, db: Session = Depends(get_db)):
    request = db.query(models.EmergencyRequest).filter(models.EmergencyRequest.request_id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    # Current Notification -> Rejected
    last_notification = db.query(models.HospitalNotification)\
        .filter(models.HospitalNotification.request_id == request_id)\
        .order_by(models.HospitalNotification.id.desc())\
        .first()
    
    if last_notification:
        last_notification.status = "Rejected"

    # History Check
    previous_notifications = db.query(models.HospitalNotification.hospital_id)\
        .filter(models.HospitalNotification.request_id == request_id).all()
    rejected_hospital_ids = [n[0] for n in previous_notifications]

    # Find Next Nearest
    all_hospitals = db.query(models.Hospital).filter(models.Hospital.supports_emergency == True).all()
    
    hospital_distances = []
    for h in all_hospitals:
        #  Smart Distance here too
        dist = get_best_distance(request.latitude, request.longitude, h.latitude, h.longitude)
        hospital_distances.append((h, dist))
    
    hospital_distances.sort(key=lambda x: x[1])

    next_hospital = None
    for h, dist in hospital_distances:
        if h.id not in rejected_hospital_ids:
            next_hospital = h
            break 
    
    if not next_hospital:
        return {"message": "CRITICAL: No other hospitals available!", "status": "Failed"}

    # Re-route
    request.hospital_id = next_hospital.id
    
    new_notif = models.HospitalNotification(
        request_id=request.request_id,
        hospital_id=next_hospital.id,
        status="Pending"
    )
    db.add(new_notif)
    db.commit()

    return {
        "message": f"Request moved to next hospital: {next_hospital.name}",
        "new_hospital": next_hospital.name,
        "status": "Re-routed",
        "hospital_lat": next_hospital.latitude,
        "hospital_lng": next_hospital.longitude
    }


#  UTILITY

@app.get("/api/hospitals")
def get_hospitals(db: Session = Depends(get_db)):
    hospitals = db.query(models.Hospital).all()
    return hospitals