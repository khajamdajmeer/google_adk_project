import sys
import os
import uuid
import random
from datetime import datetime, date, time, timedelta

# Ensure the app directory is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.session import engine, SessionLocal
from app.db.schemas.doctors_schemas import Base, DoctorORM, PatientORM, AppointmentORM, AppointmentStatus

def seed_data():
    print("Creating tables if they don't exist...")
    # This ensures the doctors, patients, and appointments tables are created 
    # if they haven't been migrated yet.
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Check if data already exists to avoid duplication errors
        existing_doctors = db.query(DoctorORM).count()
        if existing_doctors > 0:
            print(f"Database already contains {existing_doctors} doctors. Skipping seeding.")
            return

        print("Generating fake data...")
        
        # 1. Create Doctors
        doctors = [
            DoctorORM(
                id=uuid.uuid4(),
                name=name,
                specialization=spec,
                is_active=True,
                created_at=datetime.utcnow()
            )
            for name, spec in [
                ("Alice Smith", "Cardiologist"),
                ("Bob Jones", "Neurologist"),
                ("Charlie Brown", "General Practitioner"),
                ("Diana Prince", "Pediatrician")
            ]
        ]
        db.add_all(doctors)

        # 2. Create Patients
        patients = [
            PatientORM(
                id=uuid.uuid4(),
                name=name,
                email=f"{name.split()[0].lower()}@example.com",
                phone=f"555-{random.randint(1000, 9999)}",
                created_at=datetime.utcnow()
            )
            for name in [
                "Eve Adams", "Frank Castle", "Grace Hopper", "Hank Pym",
                "Ivy Pepper", "Jack Bauer", "Karen Page", "Luke Cage"
            ]
        ]
        db.add_all(patients)
        
        # Commit patients and doctors first to satisfy foreign key constraints 
        # when we create the appointments.
        db.commit()

        # 3. Create Appointments
        statuses = ["booked", "confirmed", "cancelled", "completed", "rescheduled"]
        appointments = []
        
        # Generate appointments over the next 7 days
        today = date.today()
        for _ in range(20):
            doc = random.choice(doctors)
            pat = random.choice(patients)
            
            # Random date within the next 7 days
            app_date = today + timedelta(days=random.randint(0, 7))
            
            # Random time between 9 AM and 4 PM
            app_time = time(random.randint(9, 16), random.choice([0, 30]))
            
            app = AppointmentORM(
                id=uuid.uuid4(),
                doctor_id=doc.id,
                patient_id=pat.id,
                appointment_date=app_date,
                appointment_time=app_time,
                status=random.choice(statuses),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            appointments.append(app)

        db.add_all(appointments)
        db.commit()
        print(f"Successfully seeded: \n- {len(doctors)} doctors\n- {len(patients)} patients\n- {len(appointments)} appointments.")

    except Exception as e:
        db.rollback()
        print(f"An error occurred while seeding: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
