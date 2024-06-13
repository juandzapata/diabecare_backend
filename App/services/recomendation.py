from exceptions.not_created import NotCreatedException
from utils.constants.default_values import COUNT_ELEMENTS_ZERO, NOT_ID
from data.repositories.recommendation_repository import RecommendationRepository
from schemas.recommendation import RecommendationCreate, RecommendationOut
from data.models.base import Recomendacion

class RecommendationService:
    def __init__(self, db):
        self.recommendation_repository = RecommendationRepository(db)
        
    def post_recommendation (self, recommendation: RecommendationCreate) -> RecommendationOut | NotCreatedException:
            """
            Creates a new recommendation.

            Args:
                recommendation (RecommendationCreate): The recommendation data to be created.

            Returns:
                RecommendationOut: The created recommendation.

            Raises:
                NotCreatedException: If the recommendation could not be created.
            """
            recommendation = self.recommendation_repository.post_recommendation(recommendation)
            if recommendation:
                return recommendation
            raise NotCreatedException("La recomendación no pudo ser creada")

    def get_recommendations_by_plan_id(self, plan_id: int) -> list[Recomendacion] | None:
            """
            Retrieves a list of recommendations based on the given plan ID.

            Args:
                plan_id (int): The ID of the plan.

            Returns:
                list[Recommendation] | None: A list of recommendations or None if no recommendations are found.
            """
            recommendations = self.recommendation_repository.get_recomendations_by_plan_id(plan_id)
            return recommendations