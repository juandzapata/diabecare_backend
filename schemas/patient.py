from datetime import date
from pydantic.types import Decimal
from pydantic import BaseModel

class PacientList(BaseModel):
    patient_id: int
    name: str
    last_name: str
    date: date
    age: int
    glucose_level: Decimal
    physical_activity_hours: Decimal
    last_medication: str
    last_meal: str
    photo: str

class PatientPlan(BaseModel):
    patient_id: int
    full_name: str

class PatientHistoryCreate(BaseModel):
    patient_id: int
    glucose_level: int
    physical_activity_hours: int
    last_medication: str
    last_meal: str

class PatientHistoryRead(BaseModel):
    id: int
    patient_id: int
    recorded_at: str
    glucose_level: int
    physical_activity_hours: int
    last_medication: str
    last_meal: str

    class Config:
        orm_mode = True
