from fastapi import APIRouter, HTTPException
from sqlmodel import SQLModel, Field, Session, select
from database import engine


@router.get("/dossier/{patient_id}")
def get_dossier:(patient_id)
    return{dossier_patient}

@app.get("/patient/")
async def get_patient():
    return service.get_all_patient()