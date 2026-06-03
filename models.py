from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, date

class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    nom: str
    prenom: str
    email: str = Field(unique=True, index=True)
    password: str
    role: Optional[str] = None
    created_at: Optional[datetime] = None


class Patient(SQLModel, table=True):
    __tablename__ = "Patients"
    __table_args__ = {"extend_existing": True}
    
    id_patient: Optional[int] = Field(default=None, primary_key=True)
    nom: str
    prenom: str
    num_secu: Optional[str] = None  
    email: Optional[str] = None
    mdp: Optional[str] = None
    id_user: Optional[int] = None  

class Medecin(SQLModel, table=True):
    __tablename__ = "Medecins"
    __table_args__ = {"extend_existing": True}
    
   
    id_medecin: Optional[int] = Field(default=None, primary_key=True)
    nom: str
    prenom: str
    specialite: str

class Rendezvous(SQLModel, table=True):
    __tablename__ = "RendezVous"
    __table_args__ = {"extend_existing": True}
    
    id_rdv: Optional[int] = Field(default=None, primary_key=True)
    id_patient: Optional[int] = Field(default=None, foreign_key="Patients.id_patient")
    id_medecin: Optional[int] = Field(default=None, foreign_key="Medecins.id_medecin")
    date_rdv: Optional[date] = None
    heure: Optional[str] = None
    statut: Optional[str] = "En attente"

class Ordonnance(SQLModel, table=True):
    __tablename__ = "ordonnances"
    __table_args__ = {"extend_existing": True}
    
    id_ordonnance: Optional[int] = Field(default=None, primary_key=True)
    id_patient: int = Field(foreign_key="Patients.id_patient")
    id_medecin: int = Field(foreign_key="Medecins.id_medecin")
    contenu: Optional[str] = None
    date_ordonnance: Optional[date] = None