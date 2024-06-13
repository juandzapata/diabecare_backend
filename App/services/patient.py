from services.pdf import PdfService
from services.health_professional import HealthProfessionalService
from schemas.pdf import DataReportCreate
from utils.exceptions.not_exists import NotExistsException
from utils.mappers.patient_history_mapper import PatientHistoryMapper
from data.repositories.patient_repository import PatientRepository
from utils.constants.default_values import NOT_ID
from data.models.base import Paciente, ProfesionalSalud, Usuario 
from schemas.patient import PatientList, PatientDataReport, PatientHistoryCreate, PatientHistoryRead


class PatientService:
    def __init__(self, db):
        self.patient_repository = PatientRepository(db)
        self.db = db

   
    def generate_pdf(self, data_report: DataReportCreate):
            """
            Generates a PDF report for a patient.

            Args:
                data_report (DataReportCreate): The data required to generate the report. 
                Includes the patient ID and the user ID of the professional who wants to generate 
                the report

            Returns:
                pdf_buffer: The generated PDF report as a buffer.
    """
            patient_data = self.get_data_for_pdf(data_report)
            service_pdf = PdfService()
            pdf_buffer = service_pdf.generate_pdf(patient_data)
            return pdf_buffer
        
    def create_history(self, history_create: PatientHistoryCreate) -> PatientHistoryRead:
        """
        Creates a new patient history.

        Args:
            history_create (PatientHistoryCreate): The data required to create the patient history.

        Returns:
            PatientHistoryRead: The created patient history.

        Raises:
            SomeException: If there is an error during the creation of the patient history.
            For example, data types or the patient for whom the history is created does not exist. 
        """
        patient = self.get_patient_by_user_id(history_create.user_patient_id)
        history_create.patient_id = patient.pacienteId
        history = PatientHistoryMapper.to_patient_history_model(history_create)
        created_history = self.patient_repository.create(history)
        return PatientHistoryRead.model_validate(created_history)

    def get_info_patients_by_professional_id(self, professional_id: int) -> list[PatientList]:
        """
        Retrieves information about patients based on the professional ID.

        Args:
            professional_id (int): The ID of the professional.

        Returns:
            list[PatientList]: A list of patients matching the professional ID.
        """
        if professional_id != NOT_ID:
            patients = self.patient_repository.get_patients_by_professional_id(professional_id)
            return patients

    def get_user_patient_by_id(self, patient_id: int) -> Usuario | NotExistsException:
        """
        Retrieves the user associated with the given patient ID.

        Args:
            patient_id (int): The ID of the patient.

        Returns:
            Usuario | NotExistsException: The user associated with the patient ID, or a NotExistsException if no user is found.

        Raises:
            NotExistsException: If no user is found for the given patient ID.
        """
        user = self.patient_repository.user_by_patient_id(patient_id)
        if user:
            return user
        raise NotExistsException(f"No existe un usuario asociado al paciente con id {patient_id}")
    
    def get_patient_by_user_id(self, user_id: int) -> Paciente | NotExistsException:
        """
        Retrieves a patient by their user ID.

        Args:
            user_id (int): The ID of the user associated with the patient.

        Returns:
            Paciente | NotExistsException: The patient object if found, or a NotExistsException if not found.

        Raises:
            NotExistsException: If no patient is found with the given user ID.
        """
        patient = self.patient_repository.get_patient_by_user_id(user_id)
        if patient:
            return patient
        raise NotExistsException(f"No existe un paciente con el id de usuario {user_id}")
    
    def get_data_report(self, patient_id: int, professional: ProfesionalSalud) -> PatientDataReport | NotExistsException:
        """
        Retrieves the data report for a specific patient.

        Args:
            patient_id (int): The ID of the patient.
            professional (ProfesionalSalud): The healthcare professional associated with the report.

        Returns:
            PatientDataReport: The data report for the patient.

        Raises:
            NotExistsException: If no patient with the given ID exists.
        """
        patient_data = self.patient_repository.get_data_report(patient_id)
        if patient_data:
            patient_data.full_name_professional = professional
            return patient_data
        raise NotExistsException(f"No existe un paciente con el id {patient_id}")
    
    def get_data_for_pdf(self, data: DataReportCreate) -> PatientDataReport | NotExistsException:
            """
            Retrieves the necessary data to generate a PDF report for a patient.

            Args:
                data (DataReportCreate): The data required to generate the report.

            Returns:
                PatientDataReport | NotExistsException: The patient data report if it exists, otherwise a NotExistsException.
                Also, the exception can be generated if the user ID does not correspond to a professional or if the patient is not assigned to said professional.
            """
            professional_service = HealthProfessionalService(self.db)
            professional = professional_service.get_professional_by_user_id(data.professional_user_id)
            professional_service.get_professional_patient(data.patient_id, professional.profesionalSaludId)
            user_professional = professional_service.get_user_professional_by_id(professional.profesionalSaludId)
            data_report = self.get_data_report(data.patient_id, professional)
            data_report.full_name_professional = user_professional.nombre + " " + user_professional.apellidos
            data_report.email_professional = user_professional.correo
            return data_report
    
    def get_patient_by_id(self, patient_id: int) -> Paciente | NotExistsException:
            """
            Retrieves a patient by their ID.

            Args:
                patient_id (int): The ID of the patient to retrieve.

            Returns:
                Paciente | NotExistsException: The patient object if found, or a NotExistsException if the patient does not exist.

            Raises:
                NotExistsException: If no patient with the specified ID exists.
            """
            patient = self.patient_repository.get_patient_by_id(patient_id)
            if patient:
                return patient
            raise NotExistsException(f"No existe un paciente con el id {patient_id}")
