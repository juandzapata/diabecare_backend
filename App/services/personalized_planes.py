from services.health_professional import HealthProfessionalService
from exceptions.not_exists import NotExistsException
from services.recomendation import RecommendationService
from data.repositories.recommendation_repository import RecommendationRepository
from exceptions.not_created import NotCreatedException
from data.models.base import PlanesPersonalizados
from utils.constants.default_values import COUNT_ELEMENTS_ZERO
from services.patient import PatientService
from data.repositories.personalized_planes_repository import PersonalizedPlanesRepository
from fastapi import HTTPException
from schemas.personalized_planes import PersonalizedPlanCreate, PersonalizedPlanList, PersonalizedPlanOut


class PersonalizedPlanesService:
    def __init__(self, db):
        self.planes_repository = PersonalizedPlanesRepository(db)
        self.db = db
        
    def post_personalized_plan (self, plan: PersonalizedPlanCreate) -> PlanesPersonalizados | NotCreatedException:
        professional_repository = HealthProfessionalService(self.db)
        profesionalPaciente = professional_repository.get_professional_patient(plan.pacienteId, plan.profesionalSaludId)
        plan_created = self.planes_repository.post_personalized_plan(plan, profesionalPaciente.profesionalPacienteId)
        if plan_created:
            self.create_recommendations_for_plan(plan, plan_created.planId)
            return plan_created
        raise NotCreatedException("El plan no pudo ser creado.")
    
    def get_planes_by_user_id(self, user_id: int) -> list[PersonalizedPlanList] | NotExistsException:
        patient_service = PatientService(self.db)
        patient = patient_service.get_patient_by_user_id(user_id)
        patient_id = patient.pacienteId
        planes = self.planes_repository.get_planes_by_patient_id(patient_id)
        return planes
        
    def create_recommendations_for_plan (self, plan: PersonalizedPlanCreate, planId: int):
        recommendation_service = RecommendationService(self.db)
        for i in range(len(plan.recomendaciones)):
            plan.recomendaciones[i].planId = planId
            recommendation_service.post_recommendation(plan.recomendaciones[i])



