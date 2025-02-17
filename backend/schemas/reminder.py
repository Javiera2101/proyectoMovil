from pydantic import BaseModel

class ReminderBase(BaseModel):
    title: str
    description: str

class ReminderCreate(ReminderBase):
    pass

class Reminder(ReminderBase):
    id: int
    class Config:
        orm_mode = True
