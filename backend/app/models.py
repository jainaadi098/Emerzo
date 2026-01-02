from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.database import Base
import datetime

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    phone = Column(String, unique=True, index=True)
    gender = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    emergencies = relationship("EmergencyRequest", back_populates="user")

class Hospital(Base):
    __tablename__ = "hospitals"
    hospital_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    supports_emergency = Column(Boolean, default=True)
    contact_number = Column(String)
    notifications = relationship("HospitalNotification", back_populates="hospital")

class EmergencyRequest(Base):
    __tablename__ = "emergency_requests"
    request_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    emergency_type = Column(String, default="General")
    latitude = Column(Float)
    longitude = Column(Float)
    status = Column(String, default="Pending")
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    user = relationship("User", back_populates="emergencies")
    notifications = relationship("HospitalNotification", back_populates="emergency_request")

class HospitalNotification(Base):
    __tablename__ = "hospital_notifications"
    notification_id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("emergency_requests.request_id"))
    hospital_id = Column(Integer, ForeignKey("hospitals.hospital_id"))
    sent_time = Column(DateTime, default=datetime.datetime.utcnow)
    response_status = Column(String, default="Sent")
    emergency_request = relationship("EmergencyRequest", back_populates="notifications")
    hospital = relationship("Hospital", back_populates="notifications")