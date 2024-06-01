from services.patient import PatientService
from data.repositories.personalized_planes_repository import PersonalizedPlanesRepository
from fastapi import HTTPException
from schemas.personalized_planes import PersonalizedPlanCreate, PersonalizedPlanList, PersonalizedPlanOut


class PersonalizedPlanesService:
    def __init__(self, db):
        self.planes_repository = PersonalizedPlanesRepository(db)
        
    def post_personalized_plan (self, plan: PersonalizedPlanCreate) -> PersonalizedPlanOut:
        plan_created = self.planes_repository.post_personalized_plan(plan)
        if plan_created:
            return plan_created
        return None
    
    def get_planes_by_user_id(self, user_id: int) -> list[PersonalizedPlanList]:
        planes = self.planes_repository.get_planes_by_user_id(user_id)
        return planes
        




