from datetime import date
from data.repositories.recommendation_repository import RecommendationRepository
from data.repositories.health_professional_repository import HealthProfessionalRepository
from data.models.base import PlanesPersonalizados
from schemas.personalized_planes import PersonalizedPlanCreate, PersonalizedPlanOut


class PersonalizedPlanesRepository:
    def __init__(self, db):
        self.db = db
        
    def post_personalized_plan (self, plan: PersonalizedPlanCreate) -> PersonalizedPlanOut:
        professional_repository = HealthProfessionalRepository(self.db)
        profesionalPaciente = professional_repository.get_professional_patient(plan.pacienteId, plan.profesionalSaludId)
        if profesionalPaciente is None:
            return None
        
        db_plan: PlanesPersonalizados = PlanesPersonalizados(
            profesionalPacienteId = profesionalPaciente.profesionalPacienteId,
            fechaCreacion = date.today()
        )

        self.db.add(db_plan)
        self.db.commit()
        self.db.refresh(db_plan)
        
        self.create_recommendations_for_plan(plan, db_plan.planId)
        #notification.send_notification(plan, self.db)
        return db_plan.planId
    
    def create_recommendations_for_plan (self, plan: PersonalizedPlanCreate, planId: int) -> None:
        for i in range(len(plan.recomendaciones)):
            plan.recomendaciones[i].planId = planId
            recommendation_repository = RecommendationRepository(self.db)
            recommendation_repository.post_recomendation(plan.recomendaciones[i])