# routes/reminder.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.reminder import Reminder
from schemas.reminder import ReminderCreate, Reminder as ReminderSchema
from database import get_db
from routes.auth import SECRET_KEY, ALGORITHM
import jwt
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Función para verificar el token JWT
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return email
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/reminders/", response_model=ReminderSchema)
def create_reminder(reminder: ReminderCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_reminder = Reminder(title=reminder.title, description=reminder.description, user_email=current_user)
    db.add(db_reminder)
    db.commit()
    db.refresh(db_reminder)
    return db_reminder
