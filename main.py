from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import patients, medecins, rdv
from routers import ordonnances
from database import create_db_and_tables
from routers import auth
from models import User
import logging  
import os       


log_dir = "./logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    filename=f"{log_dir}/api_python.log", 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


app = FastAPI()


logging.info("L'API Medical a démarré. Surveillance active.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

#@app.on_event("startup")
#def on_startup():
#    create_db_and_tables()
#    logging.info("Base de données initialisée.") 

app.include_router(patients.router)
app.include_router(medecins.router)
app.include_router(rdv.router)
app.include_router(auth.router)
app.include_router(ordonnances.router)