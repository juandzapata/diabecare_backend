from pydantic import BaseModel

class RecomendacionSchema(BaseModel):
    planId: int
    estado: str
    actividad: str
    horaEjecucion: str
    titulo: str

class RecomendacionCreate(BaseModel):
    planId: int
    estado: str
    actividad: str
    titulo: str
    horaEjecucion: str

class RecomendacionOut(BaseModel):
    recomendacionId: int
