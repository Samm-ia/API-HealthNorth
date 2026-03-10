from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "mysql+pymysql://root:root@localhost:8889/healthnorthE6"


engine = create_engine(DATABASE_URL, echo=True) 
def get_session(): 
    with Session(engine) as session: yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

