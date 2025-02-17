# backend/servicios/login_google.py

from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi import HTTPException, status
from google.oauth2 import id_token
from google.auth.transport.requests import Request
from google.auth.transport import requests
from google.oauth2.id_token import verify_oauth2_token
from sqlalchemy.orm import Session
from models.usuario import Usuario
from schemas.usuario import UserResponse

# Función para verificar el token de Google
CLIENT_ID = "863154778458-518rlvmkuakb7vu044dtshf7b99dava0.apps.googleusercontent.com"

def login_with_google(id_token_str: str, db: Session):
    try:
        id_info = id_token.verify_oauth2_token(id_token_str, requests.Request(), CLIENT_ID)
        
        if 'email' not in id_info:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email no encontrado en el token.")
        
        usuario = db.query(Usuario).filter(Usuario.email == id_info['email']).first()
        if not usuario:
            usuario = Usuario(email=id_info['email'], nombre=id_info['name'])
            db.add(usuario)
            db.commit()
            db.refresh(usuario)
        
        return UserResponse(id=usuario.id, email=usuario.email, nombre=usuario.nombre)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido.")