from data.models.base import Recomendacion
from schemas.recommendation import RecommendationCreate, RecommendationOut


class RecommendationRepository:
    def __init__(self, db):
        self.db = db
        
    def post_recomendation (self, recommendation: RecommendationCreate) -> RecommendationOut:
        db_recommendation: Recomendacion = Recomendacion(**recommendation.model_dump())
        self.db.add(db_recommendation)
        self.db.commit()
        self.db.refresh(db_recommendation)
        return db_recommendation.recomendacionId
    
    def get_recomendations_by_plan_id(self, plan_id: int) -> list[Recomendacion]:
        return self.db.query(Recomendacion).filter(Recomendacion.planId == plan_id).all()