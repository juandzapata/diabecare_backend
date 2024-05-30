from typing import List
from pydantic import BaseModel
from datetime import date
from schemas.recomendation import RecomendationCreate

class PersonalizedPlanCreate(BaseModel):
    pacienteId: int
    profesionalSaludId: int
    recomendaciones: List[RecomendationCreate]

class PersonalizedPlanOut(BaseModel):
    planId: int
    
class PersonalizedPlanList(PersonalizedPlanOut):
    creation_date: date
    full_name_professional: str
    
    