from exceptions.not_exists import NotExistsException
from data.repositories.health_professional_repository import HealthProfessionalRepository
from sqlalchemy import text
from data.models.base import ProfesionalPaciente, ProfesionalSalud, Usuario
class HealthProfessionalService:
    def __init__(self, db):
        self.professional_repository = HealthProfessionalRepository(db)

    def get_professional_by_user_id(self, usuario_id: int) -> ProfesionalSalud | NotExistsException:
        professional = self.professional_repository.get_professional_by_user_id(usuario_id)
        if professional:
            return professional
        raise NotExistsException(f"No existe un profesional de salud con el id de usuario {usuario_id}")
    
    def get_user_professional_by_id(self, professional_id: int) -> Usuario | NotExistsException:
        user_professional = self.professional_repository.get_user_by_professional_id(professional_id)
        if user_professional:
            return user_professional
        raise NotExistsException(f"No existe un usuario asociado al profesional de salud con id {professional_id}")

    def get_professional_patient(self, pacienteId: int, profesionalSaludId: int) -> ProfesionalPaciente | NotExistsException:
        professional_patient = self.professional_repository.get_professional_patient(pacienteId, profesionalSaludId)
        if professional_patient:
            return professional_patient
        raise NotExistsException(f"No existe una relación entre el paciente con id {pacienteId} y el profesional de salud con id {profesionalSaludId}")