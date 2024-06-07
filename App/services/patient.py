from datetime import datetime
from exceptions.not_exists import NotExistsException
from utils.mappers.patient_history_mapper import PatientHistoryMapper
from data.repositories.patient_repository import PatientRepository
from utils.constants.default_values import COUNT_ELEMENTS_ZERO, NOT_ID
from data.models.base import Paciente, Usuario 
from schemas.patient import PatientList, PatientDataReport, PatientHistoryCreate, PatientHistoryRead, PatientPlan


class PatientService:
    def __init__(self, db):
        self.patient_repository = PatientRepository(db)

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
    
    def get_data_report(self, patient_id: int) -> PatientDataReport | None:
        patient = self.patient_repository.get_data_report(patient_id)
        if patient:
            return patient
        return None