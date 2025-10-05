import uuid
from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.db.session import get_db
from app.db.schemas.doctors_schemas import PatientORM
from app.core.logging import get_logger

logger = get_logger(__name__, log_file="logs/app.log")

def get_patient_by_id(patient_id: str) -> Optional[dict]:
    """Retrieves patient details by their UUID."""
    try:
        session = get_db()
        patient = session.query(PatientORM).filter(PatientORM.id == patient_id).first()
        if not patient:
            return None
        return {
            "id": str(patient.id),
            "name": patient.name,
            "email": patient.email,
            "phone": patient.phone
        }
    except SQLAlchemyError as e:
        logger.error(f"Error fetching patient by ID {patient_id}: {e}")
        return None
    finally:
        session.close()

def get_patient_by_email(email: str) -> Optional[dict]:
    """Retrieves patient details by their email."""
    try:
        session = get_db()
        patient = session.query(PatientORM).filter(PatientORM.email == email).first()
        if not patient:
            return None
        return {
            "id": str(patient.id),
            "name": patient.name,
            "email": patient.email,
            "phone": patient.phone
        }
    except SQLAlchemyError as e:
        logger.error(f"Error fetching patient by email {email}: {e}")
        return None
    finally:
        session.close()

def register_new_patient(name: str, email: str, phone: str = None) -> Dict[str, Any]:
    """Registers a new patient in the database."""
    try:
        session = get_db()
        
        # Check if email exists
        if email and session.query(PatientORM).filter(PatientORM.email == email).first():
            return {"error": f"Patient with email {email} already exists."}
            
        new_patient = PatientORM(
            id=uuid.uuid4(),
            name=name,
            email=email,
            phone=phone,
            created_at=datetime.utcnow()
        )
        session.add(new_patient)
        session.commit()
        
        return {
            "status": "success",
            "message": "Patient registered successfully",
            "patient_id": str(new_patient.id)
        }
    except IntegrityError as e:
        session.rollback()
        logger.error(f"Integrity Error creating patient: {e}")
        return {"error": "Failed to register patient due to duplicate or invalid data."}
    except Exception as e:
        session.rollback()
        logger.error(f"Error registering new patient: {e}")
        return {"error": f"Failed to register patient: {str(e)}"}
    finally:
        session.close()
