from services.recomendation import RecommendationService
from schemas.personalized_planes import PersonalizedPlanCreate
from data.models.base import ProfesionalPaciente, ProfesionalSalud, Usuario


class HealthProfessionalRepository:
    def  __init__(self, db):
        self.db = db
    
    ##No incluir validaciones en el repositorio
    ##Debe retornar todo el profesional, no solo el id
    def get_professional_id_by_user_id(self,usuario_id: int) -> int | None:
        result = self.db.query(ProfesionalSalud).filter(ProfesionalSalud.usuarioId == usuario_id).first()
        if result:
            return result.profesionalSaludId
        return None
    
    def get_user_by_professional_id(self, professional_id: int, db) -> Usuario:
        professional = self.db.query(ProfesionalSalud).filter(ProfesionalSalud.profesionalSaludId == professional_id).first()
        user_professional = db.query(Usuario).filter(Usuario.usuarioId == professional.usuarioId).first()
        return user_professional
    
    ##No va aqui 
    def create_recommendations_for_plan (self, plan: PersonalizedPlanCreate, planId: int) -> None:
        for i in range(len(plan.recomendaciones)):
            plan.recomendaciones[i].planId = planId
            recommendation_service = RecommendationService(self.db)
            recommendation_service.post_recomendation(plan.recomendaciones[i])

    def get_professional_patient (self, pacienteId: int, profesionalSaludId: int) -> ProfesionalPaciente:
        return self.db.query(ProfesionalPaciente).filter(ProfesionalPaciente.pacienteId == pacienteId, ProfesionalPaciente.profesionalId == profesionalSaludId).first()