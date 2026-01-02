import sys
import os

# Dummy File Databse
# This line is crucial: It tells Python to look for the 'app' folder here
sys.path.append(os.getcwd())

from app.db.database import SessionLocal
from app.models import Hospital, User

# Connect to the Database
db = SessionLocal()

def seed_data():
    print("Starting Database Seeding...")

    # 1. Clear Old Data (To prevent duplicates)
    try:
        db.query(Hospital).delete()
        db.query(User).delete()
        print("Old data cleared.")
    except Exception:
        print("Database was empty, skipping cleanup.")

    # 2. Add Dummy Users
    users = [
        User(name="Amit Verma", phone="+919876543210", gender="Male"),
        User(name="Priya Sharma", phone="+919876543211", gender="Female")
    ]
    db.add_all(users)
    print("Users added.")

    # 3. Add Dummy Hospitals (Indore Locations)
    hospitals = [
        # Hospital 1: The closest one (Govt)
        Hospital(
            name="MY Hospital (Govt)",
            latitude=22.7196, 
            longitude=75.8577, 
            supports_emergency=True, 
            contact_number="108"
        ),
        # Hospital 2: Farther away
        Hospital(
            name="Bombay Hospital",
            latitude=22.7543, 
            longitude=75.8950, 
            supports_emergency=True, 
            contact_number="0731-2552525"
        ),
        # Hospital 3: The TRICK (Eye Clinic - AI should ignore this!)
        Hospital(
            name="Agarwal Eye Clinic",
            latitude=22.7200, 
            longitude=75.8580, 
            supports_emergency=False, 
            contact_number="0731-1234567"
        )
    ]
    
    db.add_all(hospitals)
    db.commit()
    print("Hospitals added.")
    print("\nDatabase is fully loaded and ready!")

if __name__ == "__main__":
    seed_data()