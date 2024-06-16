from services.recomendation import RecommendationService
from schemas.personalized_planes import PersonalizedPlanCreate
from data.models.base import ProfesionalPaciente, ProfesionalSalud, Usuario


class HealthProfessionalRepository:
    """
    Repository class for managing health professionals in the system.
    """

    def __init__(self, db):
        self.db = db
    
    def get_professional_by_user_id(self, usuario_id: int) -> ProfesionalSalud | None:
        result = self.db.query(ProfesionalSalud).filter(ProfesionalSalud.usuarioId == usuario_id).first()
        return result
    
    def get_user_by_professional_id(self, professional_id: int) -> Usuario:
        print("id profesional que llega", professional_id)
        professional: ProfesionalSalud = self.db.query(ProfesionalSalud).filter(ProfesionalSalud.profesionalSaludId == professional_id).first()
        user_professional = self.db.query(Usuario).filter(Usuario.usuarioId == professional.usuarioId).first()
        return user_professional
    
    def get_professional_patient (self, paciente_id: int, health_professional_id: int) -> ProfesionalPaciente:
        return self.db.query(ProfesionalPaciente).filter(ProfesionalPaciente.pacienteId == paciente_id, ProfesionalPaciente.profesionalId == health_professional_id).first()