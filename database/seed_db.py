from sqlalchemy.orm import Session


from .database import SessionLocal, engine
from backend.app import models

# 1. Sabse pehle Tables Create karein
models.Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()
    print(" Starting Database Seeding (Bhopal Data)...")

    # ---------------------------------------------------
    # 2. CLEAR OLD DATA (Safayi Abhiyan)
    # ---------------------------------------------------
    try:
        # Child Tables pehle delete hongi
        db.query(models.HospitalNotification).delete()
        db.query(models.EmergencyRequest).delete()
        
        # Parent Tables baad mein
        db.query(models.User).delete()
        db.query(models.Hospital).delete()
        
        db.commit()
        print(" Old data cleared successfully.")
    except Exception as e:
        print(f" Cleanup skipped or failed (New DB?): {e}")
        db.rollback()

    # ---------------------------------------------------
    # 3. ADD USERS (Same as before)
    # ---------------------------------------------------
    users = [
        models.User(
            full_name="Rahul Sharma", 
            email="rahul@example.com", 
            password="hashedpassword123"
        ),
        models.User(
            full_name="Priya Verma", 
            email="priya@example.com", 
            password="hashedpassword123"
        ),
        models.User(
            full_name="Amit Singh", 
            email="amit@example.com", 
            password="hashedpassword123"
        )
    ]
    db.add_all(users)
    db.commit()
    print(" Users Added")

    # 11 Hospitals are added
    
    hospitals = [
        # --- General / Emergency Hospitals ---
        models.Hospital(
            name="AIIMS Bhopal",
            latitude=23.2086,
            longitude=77.4607,
            address="Saket Nagar, Bhopal",
            contact_number="0755-2970771",
            supports_emergency=True
        ),
        models.Hospital(
            name="Bhopal Memorial Hospital (BMHRC)",
            latitude=23.2941,
            longitude=77.4242,
            address="Raisen Bypass Road, Bhopal",
            contact_number="0755-2740875",
            supports_emergency=True
        ),
        models.Hospital(
            name="Hamidia Hospital",
            latitude=23.2570,
            longitude=77.3929,
            address="Royal Market, Bhopal",
            contact_number="0755-2660233",
            supports_emergency=True
        ),
        models.Hospital(
            name="Bansal Hospital",
            latitude=23.2114,
            longitude=77.4332,
            address="Shahpura, Bhopal",
            contact_number="0755-4086000",
            supports_emergency=True
        ),
        models.Hospital(
            name="Chirayu Medical College & Hospital",
            latitude=23.2831,
            longitude=77.3364,
            address="Bhopal-Indore Highway",
            contact_number="0755-2709101",
            supports_emergency=True
        ),
        models.Hospital(
            name="Jai Prakash (JP) District Hospital",
            latitude=23.2356,
            longitude=77.4005,
            address="Tulsi Nagar, Bhopal",
            contact_number="0755-2551151",
            supports_emergency=True
        ),
        models.Hospital(
            name="Narmada Trauma Centre",
            latitude=23.2201,
            longitude=77.4367,
            address="Hoshangabad Road, Bhopal",
            contact_number="0755-4040000",
            supports_emergency=True
        ),
        models.Hospital(
            name="J.K. Hospital (LN Medical College)",
            latitude=23.1765,
            longitude=77.4124,
            address="Kolar Road, Bhopal",
            contact_number="0755-4087000",
            supports_emergency=True
        ),
        
        # --- No Emergency Support / Specialized ---
        models.Hospital(
            name="ASG Eye Hospital",
            latitude=23.2335,
            longitude=77.4295,
            address="M.P. Nagar, Bhopal",
            contact_number="0755-4082000",
            supports_emergency=False # No Emergency
        ),
        models.Hospital(
            name="Rishiraj College of Dental Sciences",
            latitude=23.3050,
            longitude=77.3370,
            address="Gandhinagar, Bhopal",
            contact_number="0755-6647306",
            supports_emergency=False # No Emergency
        ),
        models.Hospital(
            name="Govt. Homoeopathic Medical College",
            latitude=23.2160,
            longitude=77.4080,
            address="Kaliasot Dam, Bhopal",
            contact_number="0755-2551525",
            supports_emergency=False # No Emergency
        )
    ]
    db.add_all(hospitals)
    db.commit()
    print(f" {len(hospitals)} Hospitals Added")

    print(" Database seeded successfully!")
    db.close()

if __name__ == "__main__":
    seed_data()