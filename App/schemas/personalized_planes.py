from typing import List
from pydantic import BaseModel
from datetime import date
from schemas.recommendation import RecommendationCreate

class PersonalizedPlanCreate(BaseModel):
    pacienteId: int
    profesionalSaludId: int
    recomendaciones: List[RecommendationCreate] 

class PersonalizedPlanOut(BaseModel):
    planId: int
    profesionalPacienteId: int
    fechaCreacion: date

    class Config:
        orm_mode = True
        from_attributes = True


    
class PersonalizedPlanList(PersonalizedPlanOut):
    creation_date: date
    full_name_professional: str
    
    