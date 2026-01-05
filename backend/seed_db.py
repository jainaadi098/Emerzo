import sys
import os

# Ensure we can find the 'app' folder
sys.path.append(os.getcwd())

from app.db.database import SessionLocal
from app.models import Hospital, User

# Connect to Database
db = SessionLocal()

def seed_data():
    print("🌱 Starting Database Seeding (Bhopal Data)...")

    # 1. Clear Old Data
    try:
        db.query(Hospital).delete()
        db.query(User).delete()
        print("🧹 Old data cleared.")
    except Exception:
        print("⚠️  Database empty, skipping cleanup.")

    # 2. Add Dummy Users
    users = [
        User(name="Rahul Sharma", phone="+919999999991", gender="Male"),
        User(name="Priya Singh", phone="+919999999992", gender="Female")
    ]
    db.add_all(users)

    # 3. Add 11 Bhopal Hospitals
    hospitals = [
        # --- General / Emergency Hospitals (TRUE) ---
        Hospital(
            name="AIIMS Bhopal",
            latitude=23.2086,
            longitude=77.4607,
            supports_emergency=True,
            contact_number="0755-2970771"
        ),
        Hospital(
            name="Bhopal Memorial Hospital (BMHRC)",
            latitude=23.2941,
            longitude=77.4242,
            supports_emergency=True,
            contact_number="0755-2740875"
        ),
        Hospital(
            name="Hamidia Hospital",
            latitude=23.2570,
            longitude=77.3929,
            supports_emergency=True,
            contact_number="0755-2660233"
        ),
        Hospital(
            name="Bansal Hospital",
            latitude=23.2114,
            longitude=77.4332,
            supports_emergency=True,
            contact_number="0755-4086000"
        ),
        Hospital(
            name="Chirayu Medical College & Hospital",
            latitude=23.2831,
            longitude=77.3364,
            supports_emergency=True,
            contact_number="0755-2709101"
        ),
        Hospital(
            name="Jai Prakash (JP) District Hospital",
            latitude=23.2356,
            longitude=77.4005,
            supports_emergency=True,
            contact_number="0755-2551151"
        ),
        Hospital(
            name="Narmada Trauma Centre",
            latitude=23.2201,
            longitude=77.4367,
            supports_emergency=True,
            contact_number="0755-4040000"
        ),
        Hospital(
            name="J.K. Hospital (LN Medical College)",
            latitude=23.1765,
            longitude=77.4124,
            supports_emergency=True,
            contact_number="0755-4087000"
        ),

        # --- No Emergency Support / Specialized (FALSE) ---
        Hospital(
            name="ASG Eye Hospital",
            latitude=23.2335,
            longitude=77.4295,
            supports_emergency=False,  # This will be ignored by AI
            contact_number="0755-4082000"
        ),
        Hospital(
            name="Rishiraj College of Dental Sciences",
            latitude=23.3050,
            longitude=77.3370,
            supports_emergency=False,  # This will be ignored by AI
            contact_number="0755-6647306"
        ),
        Hospital(
            name="Govt. Homoeopathic Medical College",
            latitude=23.2160,
            longitude=77.4080,
            supports_emergency=False,  # This will be ignored by AI
            contact_number="0755-2551525"
        )
    ]
    
    db.add_all(hospitals)
    db.commit()
    print(f"✅ {len(hospitals)} Bhopal Hospitals added successfully!")
    print("\n🎉 Database is ready!")

if __name__ == "__main__":
    seed_data()