from pydantic import BaseModel

class RecomendacionCreate(BaseModel):
    planId: int
    estado: str = 'Sin realizar'
    actividad: str
    titulo: str
    horaEjecucion: str

class RecomendacionOut(BaseModel):
    recomendacionId: int
