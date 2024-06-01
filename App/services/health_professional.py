from data.repositories.health_professional_repository import HealthProfessionalRepository
from services.patient import PatientService
from sqlalchemy import text
from data.models.base import ProfesionalSalud, Usuario
from schemas.patient import PacientList
from sqlalchemy.orm import Session
from utils.constants.default_values import NOT_ID, COUNT_ELEMENTS_ZERO

class HealthProfessionalService:
    def __init__(self, db):
        self.professional_repository = HealthProfessionalRepository(db)

    def get_professional_id_by_user_id(self, usuario_id: int) -> int | None:
        professional_id = self.professional_repository.get_professional_id_by_user_id(usuario_id)
        if professional_id:
            return professional_id
        return None
    
    def get_user_professional_by_id(self, professional_id) -> Usuario:
        user_professional = self.professional_repository.get_user_by_professional_id(professional_id)
        if user_professional:
            return user_professional
        return None
