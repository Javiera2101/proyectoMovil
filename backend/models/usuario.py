from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from models.reminder import Reminder  # Importa el modelo
from datetime import datetime, timezone

class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))  # Usando timezone.utc

    def __repr__(self):
        return f"<Usuario(username={self.username}, email={self.email})>"