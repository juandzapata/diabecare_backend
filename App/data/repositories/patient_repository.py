from datetime import date
from sqlalchemy import text
from utils.mappers.patient_data_report_mapper import PatientDataReportMapper
from utils.mappers.patient_list_mapper import PatientListMapper
from schemas.patient import PatientList, PatientDataReport
from utils.constants.query import QUERY_GET_DATA_REPORT, QUERY_GET_INFO_PATIENTS_BY_PROFESSIONAL_ID, QUERY_GET_PATIENT_BY_ID, QUERY_GET_USER_PATIENT_BY_ID
from data.models.base import HistorialDatos, Paciente, Usuario


class PatientRepository:
    def __init__(self, db):
        self.db = db

    def create(self, history: HistorialDatos) -> HistorialDatos:
        self.db.add(history)
        self.db.commit()
        self.db.refresh(history)
        return history

    def get_history_by_patient_id(self, patient_id: int):
        return self.db.query(HistorialDatos).filter(HistorialDatos.pacienteId == patient_id).all()
    
    def get_patients_by_professional_id(self, professional_id: int) -> list[PatientList]:
        query = text(QUERY_GET_INFO_PATIENTS_BY_PROFESSIONAL_ID)
        patients = self.db.execute(query, {"professional_id": professional_id}).fetchall()
        
        patients_list = []
        
        for patient in patients:
            patient = PatientListMapper.to_patient_list_model(patient)
            patients_list.append(patient)
        
        return patients_list 
    
    def user_by_patient_id(self, patient_id: int) -> Usuario:
        user_db = self.db.query(Usuario).join(Paciente, Paciente.usuarioId == Usuario.usuarioId).filter(Paciente.pacienteId == patient_id).first()
        return user_db
    
    def get_patient_by_user_id(self, user_id: int) -> Paciente:
        patient = self.db.query(Paciente).filter(Paciente.usuarioId == user_id).first()
        return patient
    
    def get_data_report(self, patient_id: int) -> PatientDataReport:
        query = text(QUERY_GET_DATA_REPORT)
        data_patient = self.db.execute(query, {"patient_id": patient_id}).fetchone()
        patient = PatientDataReportMapper.to_patient_data_report_model(data_patient)
        return patient