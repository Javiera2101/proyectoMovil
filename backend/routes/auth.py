# routes/auth.py
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from models.usuario import Usuario  # Asegúrate de tener tu modelo de Usuario
from sqlalchemy.orm import Session
from database import get_db
from schemas.usuario import UsuarioCreate  # Asegúrate de que esté en el archivo correcto
from datetime import datetime, timedelta, timezone

# Configuración de passlib para manejar contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "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"  # Cambia esto por algo más seguro
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()

class Token(BaseModel):
    access_token: str
    token_type: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True

# Función para crear un token JWT
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta  # Cambiar a timezone-aware datetime
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/register", response_model=UserResponse)  # Asegúrate de que UsuarioResponse esté definido correctamente
async def register_user(user: UsuarioCreate, db: Session = Depends(get_db)):
    # Verifica si el usuario ya existe
    db_user = db.query(Usuario).filter(Usuario.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Crea el nuevo usuario
    hashed_password = pwd_context.hash(user.password)
    new_user = Usuario(email=user.email, password=hashed_password)
    
    # Agrega el usuario a la base de datos
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully", "user": new_user}


# Ruta para hacer login y generar el JWT
@router.post("/login", response_model=Token)
def login_for_access_token(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(Usuario).filter(Usuario.email == user.email).first()
    
    if db_user is None or not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    access_token = create_access_token(
        data={"sub": db_user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}
