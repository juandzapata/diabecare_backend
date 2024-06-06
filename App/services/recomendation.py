from utils.constants.default_values import COUNT_ELEMENTS_ZERO, NOT_ID
from data.repositories.recommendation_repository import RecommendationRepository
from schemas.recommendation import RecommendationCreate, RecommendationOut
from data.models.base import Recomendacion

class RecommendationService:
    def __init__(self, db):
        self.recommendation_repository = RecommendationRepository(db)
        
    def post_recommendation (self, recommendation: RecommendationCreate) -> RecommendationOut:
        recommendation = self.recommendation_repository.post_recommendation(recommendation)
        if recommendation != NOT_ID:
            return recommendation
        return None

    def get_recommendations_by_plan_id(self, plan_id: int) -> list[Recomendacion] | None:
        recommendations = self.recommendation_repository.get_recomendations_by_plan_id(plan_id)
        if len(recommendations) > COUNT_ELEMENTS_ZERO:
            return recommendations
        return None