from sqlalchemy import Column, Integer, String, Float
from database import Base

class Hospital(Base):
    __tablename__ = "hospitals"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    emergency = Column(Integer)
    phone = Column(String)
