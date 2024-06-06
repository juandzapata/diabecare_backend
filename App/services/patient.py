from datetime import datetime
from utils.mappers.patient_history_mapper import PatientHistoryMapper
from data.repositories.patient_repository import PatientRepository
from utils.constants.default_values import COUNT_ELEMENTS_ZERO, NOT_ID
from data.models.base import Usuario 
from schemas.patient import PacientList, PatientDataReport, PatientHistoryCreate, PatientHistoryRead, PatientPlan


class PatientService:
    def __init__(self, db):
        self.patient_repository = PatientRepository(db)

    def create_history(self, history_create: PatientHistoryCreate) -> PatientHistoryRead:
        patient_id = self.get_patient_id_by_user_id(history_create.user_patient_id)
        history_create.patient_id = patient_id
        history = PatientHistoryMapper.to_patient_history_model(history_create)
        created_history =  self.patient_repository.create(history)
        return PatientHistoryRead.model_validate(created_history)

    def get_info_patients_by_professional_id(self, professional_id: int) -> list[PacientList]:
        if professional_id != NOT_ID:
            patients = self.patient_repository.get_patients_by_professional_id(professional_id)
            if len(patients) > COUNT_ELEMENTS_ZERO:
                return patients
        return None

    def get_user_patient_by_id(self, patient_id: int) -> Usuario:
        user = self.patient_repository.user_by_patient_id(patient_id)
        if user:
            return user
        return None

    def get_patient(self, id :int) -> PatientPlan:
        patient = self.patient_repository.get_patient_by_id(id)
        if patient:
            return patient
        return None
    
    def get_patient_id_by_user_id(self, user_id: int) -> int | None:
        patient_id = self.patient_repository.get_patient_id_by_user_id(user_id)
        if patient_id:
            return patient_id
        return None
    
    def get_data_report(self, patient_id: int) -> PatientDataReport | None:
        patient = self.patient_repository.get_data_report(patient_id)
        if patient:
            return patient
        return None