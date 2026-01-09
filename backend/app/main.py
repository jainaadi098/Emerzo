from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import math
import requests 
import datetime
import os
from dotenv import load_dotenv

# Load API Key from .env
load_dotenv()

app = FastAPI()

# --- SETTINGS & CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 1. IN-MEMORY DATA (For Demo Stability) ---

# REAL MAKRONIA HOSPITALS (Dr. Rai is Active)
hospitals_db = [
    {
        "id": 1, 
        "name": "Dr. Rai Hospital", 
        "lat": 23.8500, 
        "lng": 78.7900, 
        "available": True
    },
    {
        "id": 2, 
        "name": "Bansal Hospital Sagar", 
        "lat": 23.8562, 
        "lng": 78.7917, 
        "available": True
    }
]

# RAM Storage for Requests (Clears on restart)
active_requests = []

# Input Model
class EmergencyRequest(BaseModel):
    latitude: float
    longitude: float

# --- 2. SMART DISTANCE ENGINE (Hybrid) ---

ORS_API_KEY = os.getenv("ORS_API_KEY")

# A. Offline Math Formula (Backup)
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0 # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# B. Smart Function (API First -> Math Backup)
def get_best_distance(lat1, lon1, lat2, lon2):
    if not ORS_API_KEY or ORS_API_KEY == "YOUR_API_KEY_HERE":
        print("⚠️ No valid API Key, using Offline Math.")
        return haversine_distance(lat1, lon1, lat2, lon2)

    try:
        url = f"https://api.openrouteservice.org/v2/directions/driving-car?start={lon1},{lat1}&end={lon2},{lat2}"
        headers = {'Authorization': ORS_API_KEY}
        
        response = requests.get(url, headers=headers, timeout=2) 
        
        if response.status_code == 200:
            data = response.json()
            dist_meters = data['features'][0]['properties']['segments'][0]['distance']
            return dist_meters / 1000.0
        else:
            print(f"⚠️ API Error {response.status_code}: Switching to Math...")
            return haversine_distance(lat1, lon1, lat2, lon2)
            
    except Exception as e:
        print(f"⚠️ Connection Failed ({e}): Switching to Math...")
        return haversine_distance(lat1, lon1, lat2, lon2)


# --- 3. API ENDPOINTS ---

@app.get("/")
def read_root():
    return {"message": "Emerzo Backend is Ready !"}

# API 1: PATIENT TRIGGER
@app.post("/api/emergency")
async def trigger_emergency(request: EmergencyRequest):
    user_lat = request.latitude
    user_lng = request.longitude
    
    print(f"🚨 SOS Received: {user_lat}, {user_lng}")

    nearest_hospital = None
    min_dist = float('inf')

    for hosp in hospitals_db:
        if hosp["available"]:
            dist = get_best_distance(user_lat, user_lng, hosp["lat"], hosp["lng"])
            if dist < min_dist:
                min_dist = dist
                nearest_hospital = hosp

    if nearest_hospital:
        # Save to List
        new_req_id = len(active_requests) + 1
        new_request = {
            "id": new_req_id,
            "patient_id": f"PAT-{9000 + new_req_id}",
            "lat": user_lat,
            "lng": user_lng,
            "hospital_name": nearest_hospital["name"],
            "distance": round(min_dist, 2),
            "time": datetime.datetime.now().strftime("%H:%M:%S"),
            "status": "Pending"
        }
        active_requests.append(new_request)

        return {
            "status": "Assigned",
            "hospital": nearest_hospital["name"], 
            "hospital_lat": nearest_hospital["lat"],
            "hospital_lng": nearest_hospital["lng"],
            "distance_km": round(min_dist, 2)
        }
    
    raise HTTPException(status_code=404, detail="No hospitals found nearby")


# API 2: HOSPITAL DASHBOARD
@app.get("/api/hospital/requests")
def get_dashboard_data():
    pending_reqs = [r for r in active_requests if r["status"] == "Pending"]
    return pending_reqs


# API 3: HOSPITAL ACCEPT
@app.post("/api/hospital/accept/{req_id}")
def accept_request(req_id: int):
    for req in active_requests:
        if req["id"] == req_id:
            req["status"] = "Accepted"
            print(f"✅ Request #{req_id} Accepted by Hospital")
            return {"message": "Ambulance Dispatched", "status": "Accepted"}
    
    raise HTTPException(status_code=404, detail="Request not found")