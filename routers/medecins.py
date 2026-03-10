from fastapi import APIRouter, HTTPException
from sqlmodel import SQLModel, Field, Session, select
from database import engine

router = APIRouter()

class Medecin(SQLModel, table=True):
    id: int = Field(primary_key=True)
    nom: str
    specialite: str

# GET all medecins
@router.get("/medecins")
def get_all_medecins():
    with Session(engine) as session:
        medecins = session.exec(select(Medecin)).all()
        return medecins

# GET one medecin
@router.get("/medecins/{medecin_id}")
def get_medecin(medecin_id: int):
    with Session(engine) as session:
        medecin = session.get(Medecin, medecin_id)
        if not medecin:
            raise HTTPException(status_code=404, detail="Médecin introuvable")
        return medecin

# CREATE medecin
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
