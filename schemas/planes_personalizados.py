from typing import List
from pydantic import BaseModel
from datetime import date
from schemas.recomendacion import RecomendacionCreate

class PlanPersonalizadoCreate (BaseModel):
    pacienteId: int
    profesionalSaludId: int
    recomendaciones: List[RecomendacionCreate]

class PlanPersonalizadoOut (BaseModel):
    planId: int