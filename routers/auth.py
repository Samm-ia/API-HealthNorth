from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from models import Patient
from sqlmodel import SQLModel
from database import get_session

router = APIRouter(prefix="/auth", tags=["Auth"])

class Login(SQLModel):
    email: str
    password: str

@router.post("/login")
def login(data: Login, session: Session = Depends(get_session)):
    query = select(Patient).where(Patient.email == data.email)
    patient = session.exec(query).first()

    if not patient:
        raise HTTPException(401, "Identifiants invalides")

    if patient.mot_de_passe != data.password:
        raise HTTPException(401, "Identifiants invalides")

    return {
        "status": "success",
        "user": {
            "id": id.patient,
            "nom": patient.nom,
            "prenom": patient.prenom,
            "role": "patient"
        }
    }
