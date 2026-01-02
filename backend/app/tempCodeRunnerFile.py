from pydantic import BaseModel

# Input: Frontend humein yeh data bhejega
class EmergencyCreate(BaseModel):
    latitude: float
    longitude: float
    emergency_type: str = "General"  # Optional, default is General

# Output: Hum Frontend ko yeh jawab denge
class EmergencyResponse(BaseModel):
    message: str
    hospital_name: str
    contact_number: str
    distance_km: float
    status: str