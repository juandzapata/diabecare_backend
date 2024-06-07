from datetime import datetime
from typing import Optional
from pydantic.types import Decimal
from pydantic import BaseModel, validator

class PatientList(BaseModel):
    patient_id: int
    name: str
    last_name: str
    date: datetime
    age: Optional[int]
    glucose_level: Decimal
    physical_activity_hours: Decimal
    last_medication: str
    last_meal: str
    photo: str

class PatientPlan(BaseModel):
    patient_id: int
    full_name: str

class PatientHistoryCreate(BaseModel):
    user_patient_id: int
    patient_id: Optional[int]
    glucose_level: int
    hours_physical_activity: int
    medication: str
    food: str

class PatientHistoryRead(BaseModel):
    historialDatosId: int
    pacienteId: int
    fecha: datetime  
    nivelGlucosa: int
    horasActividadFisica: int
    medicamento: str
    comida: str

    @validator('fecha', pre=True, always=True)
    def date_of_diagnosis_to_str(cls, v):
        if isinstance(v, datetime):
            return v.isoformat()
        return v

    class Config:
        orm_mode = True
        from_attributes = True


class PatientDataReport(BaseModel):
    full_name: str
    email: str
    gender: str
    age: int
    average_glucose_level: Decimal
    average_physical_activity_hours: Decimal
    most_consumed_medication: str
    most_consumed_food: str
