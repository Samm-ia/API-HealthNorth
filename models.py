from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Patient(SQLModel, table=True):
    __tablename__ = "Patients"
    __table_args__ = {"extend_existing": True}
    
    id_patient: Optional[int] = Field(default=None, primary_key=True)
    nom: str
    prenom: str
    num_secu: Optional[str] = None  # 👈 ajouté
    email: str = Field(unique=True, index=True)
    mdp: str  # 👈 mot de passe (attention : en clair, mais pour l'examen ça passe)
    # ⚠️ On enlève telephone qui n'existe pas !

class Medecin(SQLModel, table=True):
    __tablename__ = "Medecins"
    __table_args__ = {"extend_existing": True}
    
    # À adapter selon la structure réelle de ta table Medecins
    id_medecin: Optional[int] = Field(default=None, primary_key=True)
    nom: str
    prenom: str
    specialite: str

class Rendezvous(SQLModel, table=True):
    __tablename__ = "RendezVous"
    __table_args__ = {"extend_existing": True}
    
    # À adapter selon ta table RendezVous
    id_rdv: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="Patients.id_patient")
    medecin_id: int = Field(foreign_key="Medecins.id_medecin")
    date_rdv: datetime
    motif: str
    statut: Optional[str] = "prévu"