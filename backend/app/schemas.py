from pydantic import BaseModel, Field
from typing import Optional

# 1. User Data lene ke liye
class EmergencyCreate(BaseModel):
    # Validation: Lat -90 se 90, Long -180 se 180 ke beech hona chahiye
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    emergency_type: str = "General"

# 2. Jawab dene ke liye (Navigation Data Added )
class EmergencyResponse(BaseModel):
    message: str
    hospital_name: str
    distance_km: float
    status: str
    request_id: int
    
    #  Navigation ke liye Coordinates
    hospital_lat: float
    hospital_lng: float