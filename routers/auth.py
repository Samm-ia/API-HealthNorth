from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from models import Patient
from sqlmodel import SQLModel
from database import get_session
from models import User

router = APIRouter(prefix="/auth", tags=["Auth"])

class Login(SQLModel):
    email: str
    password: str

@router.post("/login")
def login(data: Login, session: Session = Depends(get_session)):
    query = select(User).where(User.email == data.email)
    user = session.exec(query).first()

    if not user:
        raise HTTPException(401, "Identifiants invalides")

    if user.password != data.password:
        raise HTTPException(401, "Identifiants invalides")

    return {
        "status": "success",
        "user": {
            "id": user.id,
            "nom": user.nom,
            "prenom": user.prenom,
            "role": user.role
        }
    }
@router.post("/login")
def login(data: Login, session: Session = Depends(get_session)):
    query = select(Patient).where(Patient.email == data.email)
    Patient = session.exec(query).first()

    if not Patient:
        raise HTTPException(401, "Identifiants invalides")

    if Patient.password != data.password:
        raise HTTPException(401, "Identifiants invalides")

    return {
        "status": "success",
        "user": {
            "id": Patient.id,
            "nom": Patient.nom,
            "prenom": Patient.prenom,
            "role": Patient.role
        }
    }


@router.post("/register")
def register(user_data: User, session: Session = Depends(get_session)):
    statement = select(User).where(User.email == user_data.email)
    existing_user = session.exec(statement).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Cet email est déjà utilisé")

    try:
        # 1. Création de l'User
        new_user = User(
            nom=user_data.nom,
            prenom=user_data.prenom,
            email=user_data.email,
            password=user_data.password,
            role="patient" 
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        # 2. Création du Patient lié
        new_patient = Patient(
            id_user=new_user.id_, 
            nom=new_user.nom,
            prenom=new_user.prenom
        )
        session.add(new_patient)
        session.commit()

        return {"message": "Succès", "id_user": new_user.id_user}
    
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur base de données : {str(e)}")