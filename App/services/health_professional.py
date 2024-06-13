from utils.exceptions.not_exists import NotExistsException
from data.repositories.health_professional_repository import HealthProfessionalRepository
from sqlalchemy import text
from data.models.base import ProfesionalPaciente, ProfesionalSalud, Usuario
class HealthProfessionalService:
    def __init__(self, db):
        self.professional_repository = HealthProfessionalRepository(db)

    def get_professional_by_user_id(self, usuario_id: int) -> ProfesionalSalud | NotExistsException:
            """
            Retrieves a health professional by their user ID.

            Args:
                usuario_id (int): The ID of the user associated with the health professional.

            Returns:
                ProfesionalSalud | NotExistsException: The health professional object if found, or a NotExistsException if not found.
            """
            professional = self.professional_repository.get_professional_by_user_id(usuario_id)
            if professional:
                return professional
            raise NotExistsException(f"No existe un profesional de salud con el id de usuario {usuario_id}")
    
    def get_user_professional_by_id(self, professional_id: int) -> Usuario | NotExistsException:
            """
            Retrieves the user associated with the health professional by their ID.

            Args:
                professional_id (int): The ID of the health professional.

            Returns:
                Usuario | NotExistsException: The user associated with the health professional if found,
                otherwise raises a NotExistsException.

            Raises:
                NotExistsException: If no user is associated with the health professional.

            """
            user_professional = self.professional_repository.get_user_by_professional_id(professional_id)
            if user_professional:
                return user_professional
            raise NotExistsException(f"No existe un usuario asociado al profesional de salud con id {professional_id}")

    def get_professional_patient(self, patient_id: int, health_professional_id: int) -> ProfesionalPaciente | NotExistsException:
        """
        Retrieves the relationship between a patient and a health professional.

        Args:
            patient_id (int): The ID of the patient.
            health_professional_id (int): The ID of the health professional.

        Returns:
            ProfesionalPaciente | NotExistsException: The relationship between the patient and the health professional, or a NotExistsException if the relationship does not exist.

        Raises:
            NotExistsException: If there is no relationship between the patient and the health professional.
        """
        professional_patient = self.professional_repository.get_professional_patient(patient_id, health_professional_id)
        if professional_patient:
            return professional_patient
        raise NotExistsException(f"No existe una relación entre el paciente con id {patient_id} y el profesional de salud con id {health_professional_id}")