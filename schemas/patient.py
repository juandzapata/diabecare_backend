from datetime import date
from pydantic.types import Decimal
from pydantic import BaseModel

class PacienteLista(BaseModel):
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