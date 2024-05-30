from datetime import date, datetime
from pydantic.types import Decimal
from pydantic import BaseModel, validator

class PacientList(BaseModel):
    patient_id: int
    name: str
    last_name: str
    date: datetime
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
    pacienteId: int
    nivelGlucosa: int
    horasActividadFisica: int
    medicamento: str
    comida: str

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
