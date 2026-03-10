from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import SQLModel, Field, Session, select
from datetime import datetime
from typing import Optional, List

from database import get_session  
from models import Patient, Medecin  


class RendezVous(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    patient_id: int = Field(foreign_key="patient.id")
    medecin_id: int = Field(foreign_key="medecin.id")

    datetime_rdv: datetime
    motif: str

    status: str = Field(default="prévu")  # prévu / annulé

    created_at: Optional[datetime] = Field(
        default=None,
        sa_column_kwargs={"server_default": "CURRENT_TIMESTAMP"}
    )

    __table_args__ = (
        # Empêche deux RDV au même créneau pour le même médecin
        {"sqlite_autoincrement": True},
    )


class RendezVousCreate(SQLModel):
    patient_id: int
    medecin_id: int
    datetime_rdv: datetime
    motif: str


class RendezVousRead(SQLModel):
    id: int
    patient_id: int
    medecin_id: int
    datetime_rdv: datetime
    motif: str
    status: str
    created_at: datetime


# -----------------------------
#       ROUTER
# -----------------------------
router = APIRouter(prefix="/rdv", tags=["Rendez-vous"])


# -----------------------------
#   POST : créer un rendez-vous
# -----------------------------
@router.post("/", response_model=RendezVousRead)
def create_rdv(data: RendezVousCreate, session: Session = Depends(get_session)):

    # 1. Vérifier que le patient existe
    patient = session.get(Patient, data.patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient introuvable.")

    # 2. Vérifier que le médecin existe
    medecin = session.get(Medecin, data.medecin_id)
    if not medecin:
        raise HTTPException(status_code=404, detail="Médecin introuvable.")

    # 3. Vérifier que la date n'est pas dans le passé
    if data.datetime_rdv < datetime.now():
        raise HTTPException(status_code=400, detail="La date est déjà passée.")

    # 4. Vérifier que le créneau n'est pas déjà pris
    query = select(RendezVous).where(
        RendezVous.medecin_id == data.medecin_id,
        RendezVous.datetime_rdv == data.datetime_rdv,
        RendezVous.status == "prévu"
    )
    existing = session.exec(query).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Ce créneau est déjà réservé pour ce médecin."
        )

    # 5. Créer le rendez-vous
    rdv = RendezVous(
        patient_id=data.patient_id,
        medecin_id=data.medecin_id,
        datetime_rdv=data.datetime_rdv,
        motif=data.motif,
        status="prévu"
    )

    session.add(rdv)
    session.commit()
    session.refresh(rdv)

    return rdv


@router.get("/patient/{patient_id}", response_model=List[RendezVousRead])
def get_rdv_patient(patient_id: int, session: Session = Depends(get_session)):

    query = select(RendezVous).where(RendezVous.patient_id == patient_id)
    rdvs = session.exec(query).all()

    return rdvs

@router.get("/medecin/{medecin_id}", response_model=List[RendezVousRead])
def get_rdv_medecin(medecin_id: int, session: Session = Depends(get_session)):

    query = select(RendezVous).where(
        RendezVous.medecin_id == medecin_id,
        RendezVous.status == "prévu"  # seulement les RDV actifs
    )
    rdvs = session.exec(query).all()

    return rdvs


@router.delete("/{rdv_id}")
def cancel_rdv(rdv_id: int, patient_id: int, session: Session = Depends(get_session)):
    """
    patient_id est passé en query param :
    DELETE /rdv/12?patient_id=3
    """

    rdv = session.get(RendezVous, rdv_id)

    if not rdv:
        raise HTTPException(status_code=404, detail="Rendez-vous introuvable.")

    # Vérifier que le RDV appartient bien au patient
    if rdv.patient_id != patient_id:
        raise HTTPException(
            status_code=403,
            detail="Vous ne pouvez pas annuler un rendez-vous qui ne vous appartient pas."
        )

    # Mettre le status à annulé
    rdv.status = "annulé"
    session.add