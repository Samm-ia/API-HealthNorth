from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from database import engine
from models import Medecin

router = APIRouter()


@router.get("/medecins")
def get_all_medecins():
    with Session(engine) as session:
        medecins = session.exec(select(Medecin)).all()
        return medecins


@router.get("/medecins/{medecin_id}")
def get_medecin(medecin_id: int):
    with Session(engine) as session:
        medecin = session.get(Medecin, medecin_id)
        if not medecin:
            raise HTTPException(status_code=404, detail="Médecin introuvable")
        return medecin


@router.post("/medecins")
def create_medecin(medecin: Medecin):
    with Session(engine) as session:
        session.add(medecin)
        session.commit()
        session.refresh(medecin)
        return medecin

# DELETE medecin
@router.delete("/medecins/{medecin_id}")
def delete_medecin(medecin_id: int):
    with Session(engine) as session:
        medecin = session.get(Medecin, medecin_id)
        if not medecin:
            raise HTTPException(status_code=404, detail="Médecin introuvable")
        session.delete(medecin)
        session.commit()
        return {"message": "Médecin supprimé"}