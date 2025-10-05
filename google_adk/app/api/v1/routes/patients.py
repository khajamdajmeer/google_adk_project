from fastapi import APIRouter, HTTPException
from typing import Dict, Any, Optional
from pydantic import BaseModel, EmailStr
from app.db.queries.patient_queries import get_patient_by_id, get_patient_by_email, register_new_patient

router = APIRouter()

class PatientCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None

@router.get("/{patient_id}", response_model=Dict[str, Any])
def read_patient(patient_id: str):
    """Retrieve a patient's details by ID."""
    patient = get_patient_by_id(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@router.get("/email/{email}", response_model=Dict[str, Any])
def read_patient_by_email(email: str):
    """Retrieve a patient's details by email."""
    patient = get_patient_by_email(email)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@router.post("/", response_model=Dict[str, Any])
def create_patient(patient: PatientCreate):
    """Register a new patient."""
    result = register_new_patient(name=patient.name, email=patient.email, phone=patient.phone)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result
