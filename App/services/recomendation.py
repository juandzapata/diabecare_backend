from utils.constants.default_values import COUNT_ELEMENTS_ZERO, NOT_ID
from data.repositories.recommendation_repository import RecommendationRepository
from schemas.recomendation import RecomendationCreate, RecomendationOut
from data.models.base import Recomendacion

class RecommendationService:
    def __init__(self, db):
        self.recommendation_repository = RecommendationRepository(db)
        
    def post_recomendation (self, recomendation: RecomendationCreate) -> RecomendationOut:
        recommendation = self.recommendation_repository.post_recomendation(recomendation)
        if recommendation != NOT_ID:
            return recommendation
        return None

    def get_recomendarions_by_plan_id(self, plan_id: int) -> list[Recomendacion]:
        recommendations = self.recommendation_repository.get_recomendarions_by_plan_id(plan_id)
        if len(recommendations) > COUNT_ELEMENTS_ZERO:
            return recommendations
        return None