from services.notification import NotificationService
from services.health_professional import HealthProfessionalService
from utils.exceptions.not_exists import NotExistsException
from services.recomendation import RecommendationService
from utils.exceptions.not_created import NotCreatedException
from services.patient import PatientService
from data.repositories.personalized_planes_repository import PersonalizedPlanesRepository
from schemas.personalized_planes import PersonalizedPlanCreate, PersonalizedPlanList, PersonalizedPlanOut


class PersonalizedPlanesService:
    def __init__(self, db):
        self.planes_repository = PersonalizedPlanesRepository(db)
        self. notification_service = NotificationService(db)
        self.db = db
    
    def post_personalized_plan(self, plan: PersonalizedPlanCreate) -> PersonalizedPlanOut | NotCreatedException:
        """
        Creates a personalized plan for a patient.
        
        Args:
            plan (PersonalizedPlanCreate): The data required to create the personalized plan.
        Returns:
            PersonalizedPlanOut | NotCreatedException: The created personalized plan if successful, otherwise a NotCreatedException.
        Raises:
            NotCreatedException: If the plan could not be created.
        """
        professional_repository = HealthProfessionalService(self.db)
        professional_patient = professional_repository.get_professional_patient(plan.pacienteId, plan.profesionalSaludId)
        plan_created = self.planes_repository.post_personalized_plan(professional_patient.profesionalPacienteId)
        if plan_created:
            self.create_recommendations_for_plan(plan, plan_created.planId)
            self.notification_service.send_notification(plan)
            return PersonalizedPlanOut.model_validate(plan_created)
        raise NotCreatedException("El plan no pudo ser creado.")
    
    def get_planes_by_user_id(self, user_id: int) -> list[PersonalizedPlanList] | NotExistsException:
        """
        Retrieves the personalized plans associated with a user ID.

        Args:
            user_id (int): The ID of the user.

        Returns:
            list[PersonalizedPlanList] | NotExistsException: A list of personalized plans associated with the user ID,
            or a NotExistsException if the user does not exist.
        """
        patient_service = PatientService(self.db)
        patient = patient_service.get_patient_by_user_id(user_id)
        patient_id = patient.pacienteId
        planes = self.planes_repository.get_planes_by_patient_id(patient_id)
        return planes
        
    def create_recommendations_for_plan(self, plan: PersonalizedPlanCreate, plan_id: int):
        """
        Creates recommendations for a personalized plan.

        Args:
            plan (PersonalizedPlanCreate): The personalized plan object.
            plan_id (int): The ID of the plan.

        """
        recommendation_service = RecommendationService(self.db)
        for i in range(len(plan.recomendaciones)):
            plan.recomendaciones[i].planId = plan_id
            recommendation_service.post_recommendation(plan.recomendaciones[i])



