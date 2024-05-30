from schemas.recomendation import RecomendationCreate, RecomendationOut
from sqlalchemy.orm import Session
from data.models.base import Recomendacion

def post_recomendation (recomendation: RecomendationCreate, database: Session) -> RecomendationOut:
    db_recomendation: Recomendacion = Recomendacion(**recomendation.model_dump())
    database.add(db_recomendation)
    database.commit()
    database.refresh(db_recomendation)
    return db_recomendation.recomendacionId

def get_recomendarions_by_plan_id(plan_id: int, db) -> list[Recomendacion]:
    return db.query(Recomendacion).filter(Recomendacion.planId == plan_id).all()