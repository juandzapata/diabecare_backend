from services.health_professional import HealthProfessionalService
from schemas.pdf import DataReportCreate
from exceptions.not_exists import NotExistsException
from utils.mappers.patient_history_mapper import PatientHistoryMapper
from data.repositories.patient_repository import PatientRepository
from utils.constants.default_values import NOT_ID
from data.models.base import Paciente, ProfesionalSalud, Usuario 
from schemas.patient import PatientList, PatientDataReport, PatientHistoryCreate, PatientHistoryRead, PatientPlan


class PatientService:
    def __init__(self, db):
        self.patient_repository = PatientRepository(db)
        self.db = db

    def create_history(self, history_create: PatientHistoryCreate) -> PatientHistoryRead:
        patient = self.get_patient_by_user_id(history_create.user_patient_id)
        history_create.patient_id = patient.pacienteId
        history = PatientHistoryMapper.to_patient_history_model(history_create)
        created_history =  self.patient_repository.create(history)
        return PatientHistoryRead.model_validate(created_history)

    def get_info_patients_by_professional_id(self, professional_id: int) -> list[PatientList] | NotExistsException:
        if professional_id != NOT_ID:
            patients = self.patient_repository.get_patients_by_professional_id(professional_id)
            return patients

    def get_user_patient_by_id(self, patient_id: int) -> Usuario | NotExistsException:
        user = self.patient_repository.user_by_patient_id(patient_id)
        if user:
            return user
        raise NotExistsException(f"No existe un usuario asociado al paciente con id {patient_id}")
    
    def get_patient_by_user_id(self, user_id: int) -> Paciente | NotExistsException:
        patient = self.patient_repository.get_patient_by_user_id(user_id)
        if patient:
            return patient
        raise NotExistsException(f"No existe un paciente con el id de usuario {user_id}")
    
    def get_data_report(self, patient_id: int, professional: ProfesionalSalud) -> PatientDataReport | NotExistsException:
        patient_data = self.patient_repository.get_data_report(patient_id)
        if patient_data:
            patient_data.full_name_professional = professional
            return patient_data
        raise NotExistsException(f"No existe un paciente con el id {patient_id}")
    
    def get_data_for_pdf(self, data: DataReportCreate) -> PatientDataReport | NotExistsException:
        professional_service = HealthProfessionalService(self.db)
        professional = professional_service.get_professional_by_user_id(data.professional_user_id)
        professional_service.get_professional_patient(data.patient_id, professional.profesionalSaludId)
        user_professional = professional_service.get_user_professional_by_id(professional.profesionalSaludId)
        data_report = self.get_data_report(data.patient_id, professional)
        data_report.full_name_professional = user_professional.nombre + " " + user_professional.apellidos
        data_report.email_professional = user_professional.correo
        return data_report
    
    def get_patient_by_id(self, patient_id: int) -> Paciente | NotExistsException:
        patient = self.patient_repository.get_patient_by_id(patient_id)
        if patient:
            return patient
        raise NotExistsException(f"No existe un paciente con el id {patient_id}")