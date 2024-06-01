from typing import List
from pydantic import BaseModel
from datetime import date
from schemas.recomendation import RecommendationCreate

class PersonalizedPlanCreate (BaseModel):
    pacienteId: int
    profesionalSaludId: int
    recomendaciones: List[RecommendationCreate]

class PersonalizedPlanOut (BaseModel):
    planId: int