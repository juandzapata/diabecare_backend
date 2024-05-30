from pydantic import BaseModel
from utils.constants.default_values import DEFAULT_STATE_RECOMENDATION

class RecomendationCreate(BaseModel):
    planId: int
    estado: str = DEFAULT_STATE_RECOMENDATION
    actividad: str
    titulo: str
    horaEjecucion: str

class RecomendationOut(BaseModel):
    recomendacionId: int
