from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = 'sqlite:///database.db'

# Crear el motor de base de datos
engine = create_engine(DATABASE_URL, echo=True)

# Crear una sesión
Session = sessionmaker(bind=engine)
Base = declarative_base()

def create_session():
    return Session()

def update_database():
    print("## create or update database ##")
    Base.metadata.create_all(bind=engine)
