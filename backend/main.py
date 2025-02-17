from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine, get_db
from routes.reminder import router as reminder_router
from routes.auth import router as auth_router
from schemas.usuario import UsuarioBase, UsuarioCreate, Usuario
from schemas.usuario import TokenRequest, UserResponse
from sqlalchemy.orm import Session
from database import SessionLocal
from passlib.context import CryptContext

from services.login_google import login_with_google

app = FastAPI(debug=True)


# Configuración de CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ** Crear las tablas en la base de datos de manera síncrona **
Base.metadata.create_all(bind=engine)

# Registrar rutas
app.include_router(reminder_router)
app.include_router(auth_router, prefix="/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Bienvenido a mi aplicación"}

@app.post("/login-google", response_model=UserResponse)
async def login_google(request: TokenRequest, db: Session = Depends(get_db)):
    # Aquí gestionas el login con el token de Google
    return login_with_google(request.idToken, db)

@app.post("/auth/register", response_model=UserResponse)
def register(user: UsuarioCreate, db: Session = Depends(get_db)):
    # Hash the password before saving it
    hashed_password = pwd_context.hash(user.password)
    
    db_user = Usuario(username=user.username, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"id": db_user.id, "username": db_user.username, "email": db_user.email}