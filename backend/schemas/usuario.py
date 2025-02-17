# schemas/usuario.py
from pydantic import BaseModel

class UsuarioBase(BaseModel):
    username: str
    email: str

class UsuarioCreate(BaseModel):
    username: str
    email: str
    password: str

class Usuario(UsuarioBase):
    id: int

    class Config:
        orm_mode = True  # Permite que los modelos sean usados con SQLAlchemy

# Esta clase representa los datos del token de Google enviados en la solicitud de login.
class TokenRequest(BaseModel):
    idToken: str  # El token de Google

# Esta clase representa la respuesta después de un login exitoso.
class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True  # Esto es necesario para usar los modelos de SQLAlchemy