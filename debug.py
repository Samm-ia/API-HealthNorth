from sqlmodel import Session, select, text
from database import engine
from models import Patient

print("🔍 DIAGNOSTIC DE LA BASE DE DONNÉES")
print("="*50)

try:
    with Session(engine) as session:
        # Test 1 : connexion directe
        print("\n✅ Connexion à la base réussie")
        
        # Test 2 : lister les tables (avec text())
        print("\n📊 Tables dans la base :")
        result = session.execute(text("SHOW TABLES"))
        tables = result.fetchall()
        for table in tables:
            print(f"   - {table[0]}")
        
        # Test 3 : structure de la table Patients (avec text())
        print("\n📋 Colonnes de la table Patients :")
        result = session.execute(text("SHOW COLUMNS FROM Patients"))
        columns = result.fetchall()
        for col in columns:
            print(f"   - {col[0]} (type: {col[1]})")
        
        # Test 4 : compter les patients avec SQLModel
        patients = session.exec(select(Patient)).all()
        print(f"\n👥 Patients trouvés par SQLModel : {len(patients)}")
        
        # Test 5 : requête SQL brute sur Patients (avec text())
        result = session.execute(text("SELECT * FROM Patients"))
        rows = result.fetchall()
        print(f"\n📝 Patients trouvés par SQL direct : {len(rows)}")
        for row in rows:
            print(f"   - {row}")
            
except Exception as e:
    print(f"\n❌ ERREUR : {e}")
    import traceback
    traceback.print_exc()