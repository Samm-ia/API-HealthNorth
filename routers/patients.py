from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import Patient

router = APIRouter()

@router.get("/patients")
def get_all_patients(session: Session = Depends(get_session)):
    statement = select(Patient)
    patients = session.exec(statement).all()
    return patients


@router.get("/patients/{id_patient}")
def get_patient(id_patient: int, session: Session = Depends(get_session)):
    patient = session.get(Patient, id_patient)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.post("/patients")
def create_patient(patient: Patient, session: Session = Depends(get_session)):
    session.add(patient)
    session.commit()
    session.refresh(patient)
    return patient


@router.delete("/patients/{patient_id}")
def delete_patient(patient_id: int, session: Session = Depends(get_session)):
    patient = session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    session.delete(patient)
    session.commit()
    return {"message": "Patient deleted"}


@router.put("/patients/{patient_id}")
def update_patient(patient_id: int, updated_data: Patient, session: Session = Depends(get_session)):
    patient = session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    patient.name = updated_data.name
    session.add(patient)
    session.commit()
    session.refresh(patient)
    return patient