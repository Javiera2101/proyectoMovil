# backend/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexión a tu base de datos MariaDB
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:root@localhost/movilapp"

# Crear el motor de conexión
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"host": "localhost"})

# Crear una sesión de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos
Base = declarative_base()

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
