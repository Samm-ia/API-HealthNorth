from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from database import get_session 
from models import Ordonnance, Patient
from typing import List

router = APIRouter()

@router.get("/patient/{id_user}")
def get_ordonnances_patient(id_user: int, session: Session = Depends(get_session)):
    
    patient = session.exec(select(Patient).where(Patient.id_user == id_user)).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient non trouvé")
    
    
    ordonnances = session.exec(
        select(Ordonnance).where(Ordonnance.id_patient == patient.id_patient)
    ).all()
    return ordonnances

@router.delete("/{id_ordonnance}")
def delete_ordonnance(id_ordonnance: int, session: Session = Depends(get_session)):
    ordonnance_to_delete = session.get(Ordonnance, id_ordonnance)
    
    if not ordonnance_to_delete:
        raise HTTPException(status_code=404, detail="Ordonnance introuvable")
    
    session.delete(ordonnance_to_delete)
    session.commit()
    return {"message": "Ordonnance supprimée avec succès"}