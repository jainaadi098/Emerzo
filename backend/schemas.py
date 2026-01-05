from pydantic import BaseModel, Field

# ---------- Request Schemas ----------

class Location(BaseModel):
    lat: float = Field(..., example=12.9716)
    lon: float = Field(..., example=77.5946)


# ---------- Response Schemas ----------

class HospitalOut(BaseModel):
    id: int
    name: str
    lat: float
    lon: float
    phone: str | None = None
    eta_minutes: int

    class Config:
        from_attributes = True
