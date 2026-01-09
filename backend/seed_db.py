from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine
from app import models

# 1. Sabse pehle Tables Create karein
models.Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()
    print(" Starting Database Seeding (Dr. Rai + Backup Data)...")

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
    # 3. ADD USERS
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

    # ---------------------------------------------------
    # 4. ADD HOSPITALS (Total 12: 1 Active + 11 Commented)
    # ---------------------------------------------------
    hospitals = [
        # --- ✅ ACTIVE: REAL MAKRONIA HOSPITAL ---
        models.Hospital(
            name="Dr. Rai Hospital",
            latitude=23.8500,
            longitude=78.7900,
            address="10th Battalion SAF, Makroniya",
            contact_number="07582-263333",
            supports_emergency=True
        ),

        # --- ❌ INACTIVE: BACKUP BHOPAL HOSPITALS (11) ---
        
        # 1. AIIMS Bhopal
        # models.Hospital(
        #     name="AIIMS Bhopal",
        #     latitude=23.2086,
        #     longitude=77.4607,
        #     address="Saket Nagar, Bhopal",
        #     contact_number="0755-2970771",
        #     supports_emergency=True
        # ),
        
        # 2. BMHRC
        # models.Hospital(
        #     name="Bhopal Memorial Hospital (BMHRC)",
        #     latitude=23.2941,
        #     longitude=77.4242,
        #     address="Raisen Bypass Road, Bhopal",
        #     contact_number="0755-2740875",
        #     supports_emergency=True
        # ),
        
        # 3. Hamidia
        # models.Hospital(
        #     name="Hamidia Hospital",
        #     latitude=23.2570,
        #     longitude=77.3929,
        #     address="Royal Market, Bhopal",
        #     contact_number="0755-2660233",
        #     supports_emergency=True
        # ),
        
        # 4. Bansal Bhopal
        # models.Hospital(
        #     name="Bansal Hospital",
        #     latitude=23.2114,
        #     longitude=77.4332,
        #     address="Shahpura, Bhopal",
        #     contact_number="0755-4086000",
        #     supports_emergency=True
        # ),
        
        # 5. Chirayu
        # models.Hospital(
        #     name="Chirayu Medical College & Hospital",
        #     latitude=23.2831,
        #     longitude=77.3364,
        #     address="Bhopal-Indore Highway",
        #     contact_number="0755-2709101",
        #     supports_emergency=True
        # ),
        
        # 6. JP Hospital
        # models.Hospital(
        #     name="Jai Prakash (JP) District Hospital",
        #     latitude=23.2356,
        #     longitude=77.4005,
        #     address="Tulsi Nagar, Bhopal",
        #     contact_number="0755-2551151",
        #     supports_emergency=True
        # ),
        
        # 7. Narmada Trauma
        # models.Hospital(
        #     name="Narmada Trauma Centre",
        #     latitude=23.2201,
        #     longitude=77.4367,
        #     address="Hoshangabad Road, Bhopal",
        #     contact_number="0755-4040000",
        #     supports_emergency=True
        # ),
        
        # 8. JK Hospital
        # models.Hospital(
        #     name="J.K. Hospital (LN Medical College)",
        #     latitude=23.1765,
        #     longitude=77.4124,
        #     address="Kolar Road, Bhopal",
        #     contact_number="0755-4087000",
        #     supports_emergency=True
        # ),
        
        # 9. ASG Eye (Non-Emergency)
        # models.Hospital(
        #     name="ASG Eye Hospital",
        #     latitude=23.2335,
        #     longitude=77.4295,
        #     address="M.P. Nagar, Bhopal",
        #     contact_number="0755-4082000",
        #     supports_emergency=False 
        # ),
        
        # 10. Rishiraj Dental (Non-Emergency)
        # models.Hospital(
        #     name="Rishiraj College of Dental Sciences",
        #     latitude=23.3050,
        #     longitude=77.3370,
        #     address="Gandhinagar, Bhopal",
        #     contact_number="0755-6647306",
        #     supports_emergency=False 
        # ),
        
        # 11. Govt Homoeopathic (Non-Emergency)
        # models.Hospital(
        #     name="Govt. Homoeopathic Medical College",
        #     latitude=23.2160,
        #     longitude=77.4080,
        #     address="Kaliasot Dam, Bhopal",
        #     contact_number="0755-2551525",
        #     supports_emergency=False 
        # )
    ]
    
    db.add_all(hospitals)
    db.commit()
    print(f" {len(hospitals)} Hospital Added (Dr. Rai Active, 11 Backup Commented)")

    print(" Database seeded successfully!")
    db.close()

if __name__ == "__main__":
    seed_data()