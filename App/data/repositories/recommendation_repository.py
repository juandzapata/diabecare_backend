from data.models.base import Recomendacion
from schemas.recomendation import RecomendationCreate, RecomendationOut


class RecommendationRepository:
    def __init__(self, db):
        self.db = db
        
    def post_recomendation (self, recomendation: RecomendationCreate) -> RecomendationOut:
        db_recomendation: Recomendacion = Recomendacion(**recomendation.model_dump())
        self.db.add(db_recomendation)
        self.db.commit()
        self.db.refresh(db_recomendation)
        return db_recomendation.recomendacionId
    
    def get_recomendations_by_plan_id(self, plan_id: int) -> list[Recomendacion]:
        return self.db.query(Recomendacion).filter(Recomendacion.planId == plan_id).all()