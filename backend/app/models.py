from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database.database import Base

# -------------------------------------------------------
# 1. USER TABLE (Jo madad mangega)
# -------------------------------------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    
    # User ki multiple requests ho sakti hain
    emergencies = relationship("EmergencyRequest", back_populates="user")


# -------------------------------------------------------
# 2. HOSPITAL TABLE (Jo request receive karega)
# -------------------------------------------------------
class Hospital(Base):
    __tablename__ = "hospitals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    address = Column(String)
    contact_number = Column(String)
    supports_emergency = Column(Boolean, default=True)

    # Hospital ke paas multiple requests aur notifications aayenge
    requests = relationship("EmergencyRequest", back_populates="hospital")
    notifications = relationship("HospitalNotification", back_populates="hospital")


# -------------------------------------------------------
# 3. EMERGENCY REQUEST TABLE (Main Event)
# -------------------------------------------------------
class EmergencyRequest(Base):
    __tablename__ = "emergency_requests"

    request_id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    emergency_type = Column(String)
    status = Column(String, default="Pending") # Pending, Routed, Approved, Rejected
    created_at = Column(DateTime, default=datetime.utcnow)

    # --- Foreign Keys ---
    
    # Currently assigned Hospital (Jiske paas abhi request hai)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=True)
    hospital = relationship("Hospital", back_populates="requests")

    # Kis User ne mangayi?
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User", back_populates="emergencies")
    
    # History of notifications (Kaun kaun reject kar chuka hai)
    notifications = relationship("HospitalNotification", back_populates="request")


# -------------------------------------------------------
# 4. HOSPITAL NOTIFICATION TABLE (Monitoring Log) 
# -------------------------------------------------------
class HospitalNotification(Base):
    __tablename__ = "hospital_notifications"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, default="Pending") # Pending, Accepted, Rejected
    sent_time = Column(DateTime, default=datetime.utcnow)
    
    # Kis Request ke liye hai?
    request_id = Column(Integer, ForeignKey("emergency_requests.request_id"))
    request = relationship("EmergencyRequest", back_populates="notifications")

    # Kis Hospital ko bheji gayi?
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    hospital = relationship("Hospital", back_populates="notifications")