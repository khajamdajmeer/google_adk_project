from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError
from app.db.session import get_db
from app.db.schemas.doctors_schemas import DoctorORM
from app.core.logging import get_logger

logger = get_logger(__name__, log_file="logs/app.log")

def get_all_active_doctors() -> List[dict]:
    """Retrieves a list of all active doctors."""
    try:
        session = get_db()
        doctors = session.query(DoctorORM).filter(DoctorORM.is_active == True).all()
        result = [
            {
                "id": str(doc.id),
                "name": doc.name,
                "specialization": doc.specialization
            } for doc in doctors
        ]
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error fetching active doctors: {e}")
        return []
    finally:
        session.close()

def get_doctor_by_id(doctor_id: str) -> Optional[dict]:
    """Retrieves doctor details by their UUID."""
    try:
        session = get_db()
        doc = session.query(DoctorORM).filter(DoctorORM.id == doctor_id).first()
        if not doc:
            return None
        return {
            "id": str(doc.id),
            "name": doc.name,
            "specialization": doc.specialization,
            "is_active": doc.is_active
        }
    except SQLAlchemyError as e:
        logger.error(f"Error fetching doctor by ID {doctor_id}: {e}")
        return None
    finally:
        session.close()
