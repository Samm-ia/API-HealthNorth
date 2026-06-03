from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import SQLModel, Field, Session, select
from datetime import datetime
from typing import Optional, List
from datetime import date

from database import get_session  
from models import Patient, Medecin, Rendezvous

class RendezVousCreate(SQLModel):
    id_patient: int
    id_medecin: int
    date_rdv: date
    heure: str

from typing import Optional

class RendezVousRead(SQLModel):
    id_rdv: int
    id_patient: int
    id_medecin: int
    date_rdv: str
    heure: str
    statut: Optional[str] = None
router = APIRouter(prefix="/rdv", tags=["Rendez-vous"])

@router.post("/", response_model=RendezVousRead)
def create_rdv(data: RendezVousCreate, session: Session = Depends(get_session)):
    rdv = Rendezvous(
        id_patient=data.id_patient,
        id_medecin=data.id_medecin,
        date_rdv=data.date_rdv,
        motif=data.motif,
        statut="prévu"
    )
    session.add(rdv)
    session.commit()
    session.refresh(rdv)
    return rdv

@router.get("/patient/{id_user}") 
def get_rdv_patient(id_user: int, session: Session = Depends(get_session)):
    print(f"DEBUG: Recherche du patient pour id_user={id_user}")
    
    patient = session.exec(
        select(Patient).where(Patient.id_user == id_user)
    ).first()
    
    if not patient:
        print("DEBUG: Patient non trouvé")
        raise HTTPException(status_code=404, detail="Patient introuvable")
    
    print(f"DEBUG: Patient trouvé ! Son ID interne est {patient.id_patient}")
    
    query = select(Rendezvous).where(Rendezvous.id_patient == patient.id_patient)
    rdvs = session.exec(query).all()
    
    print(f"DEBUG: Nombre de RDV trouvés : {len(rdvs)}")
    return rdvs

@router.get("/medecin/{id_medecin}", response_model=List[RendezVousRead])
def get_rdv_medecin(id_medecin: int, session: Session = Depends(get_session)):
    query = select(Rendezvous).where(Rendezvous.id_medecin == id_medecin)
    rdvs = session.exec(query).all()
    return rdvs

@router.delete("/{id_rdv}")
def cancel_rdv(id_rdv: int, session: Session = Depends(get_session)):
    rdv = session.get(Rendezvous, id_rdv)
    if not rdv:
        raise HTTPException(status_code=404, detail="Rendez-vous introuvable.")
    rdv.statut = "annulé"
    session.add(rdv)
    session.commit()
    return {"message": "Rendez-vous annulé"}