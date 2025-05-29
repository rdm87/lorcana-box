from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .base import Base

# Percorso al file SQLite
DATABASE_URL = "sqlite:///./lorcana-products.db"

# Engine e Session
engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Funzione per creare tutte le tabelle
def init_db():
    Base.metadata.create_all(bind=engine)

# Dependency per ottenere la sessione
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
