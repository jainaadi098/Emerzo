# 🚑 Emerzo Backend (The AI Brain)

This is the backend server for **Emerzo**, an AI-powered emergency response system. 
It handles geolocation logic, hospital filtering, and routes emergency requests to the nearest *capable* facility using spatial algorithms.

---

## 🌟 Key Features

* **⚡ High-Performance API:** Built with **FastAPI** for lightning-fast responses.
* **🧠 Intelligent Routing:** Uses **Haversine Formula** & GPS logic to calculate real-time distances.
* **🏥 Smart Filtering:** Distinguishes between hospitals that support emergencies vs. clinics that don't.
* **📂 Modular Architecture:** Clean, scalable folder structure ready for cloud deployment.
* **🗄️ SQLite Database:** Lightweight and fast database for managing Users, Hospitals, and Requests.

---

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **Framework:** FastAPI
* **Database:** SQLite (managed via SQLAlchemy)
* **Validation:** Pydantic
* **Server:** Uvicorn

---

## ⚙️ Setup & Installation

Follow these steps to set up the "Brain" on your local machine.

### 1. Create Virtual Environment
Keep your dependencies isolated.

* **Windows (PowerShell):**
    ```powershell
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    ```

* **Mac / Linux:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

### 2. Install Dependencies
Install all required libraries including FastAPI, SQLAlchemy, and GPS tools.
```bash
pip install -r requirements.txt
🌱 Database Setup (Important)
Before running the server, you must fill the database with dummy data (Hospitals & Users).

Run the Seeding Script:

Bash

python seed_db.py
You should see a message: 🎉 Database is fully loaded!

🚀 How to Run
Make sure you are inside the backend folder:

Bash

cd backend
Start the Server:

Bash

uvicorn app.main:app --reload
Access the API Dashboard: Open your browser and go to: 👉 http://127.0.0.1:8000/docs

🧪 Testing the Emergency Button
You can test the logic directly from the dashboard:

Go to the Green Button (POST /api/emergency).

Click Try it out.

Paste this JSON (Location: Indore, Palasia Square):

JSON

{
  "latitude": 22.7200,
  "longitude": 75.8580,
  "emergency_type": "Heart Attack"
}
Result: The system should intelligently select "MY Hospital (Govt)" and ignore the nearer Eye Clinic.

📂 Folder Structure
Plaintext

backend/
 ├── app/
 │    ├── db/              # Database connection
 │    ├── main.py          # The Brain (API Routes & Logic)
 │    ├── models.py        # Database Tables
 │    └── schemas.py       # Data Validation Rules
 ├── emerzo.db             # The Database File
 ├── requirements.txt      # List of Libraries
 └── seed_db.py            # Script to load dummy data
👨‍💻 Contributors
Emerzo Team - Imagine Cup 2026


---

### ✨ Isme Naya Kya Hai?
1.  **Project Description:** Judges ko pehli line mein pata chal jayega ki yeh "Emergency System" hai.
2.  **Seeding Step:** Sabse zaroori! Agar koi naya banda (ya judge) ise run karega, toh usse pata hoga ki `python seed_db.py` chalana hai.
3.  **Correct Run Command:** Humne wahi command likhi hai jo finally work ki thi (`app.main:app`).
4.  **Testing Instructions:** Humne judges ko bataya hai ki ise test kaise karein.

Ise save kijiye aur batayein kaisa laga! 🚀
