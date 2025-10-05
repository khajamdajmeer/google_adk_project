from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from app.db.queries.doctor_queries import get_all_active_doctors, get_doctor_by_id

router = APIRouter()

@router.get("/", response_model=List[Dict[str, Any]])
def read_active_doctors():
    """Retrieve all active doctors."""
    doctors = get_all_active_doctors()
    return doctors

@router.get("/{doctor_id}", response_model=Dict[str, Any])
def read_doctor(doctor_id: str):
    """Retrieve details of a specific doctor by ID."""
    doctor = get_doctor_by_id(doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor
