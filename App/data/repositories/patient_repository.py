from datetime import date
from sqlalchemy import text
from utils.constants.default_values import NOT_ID
from schemas.patient import PacientList, PatientPlan
from utils.constants.query import QUERY_GET_INFO_PATIENTS_BY_PROFESSIONAL_ID, QUERY_GET_PATIENT_BY_ID, QUERY_GET_USER_PATIENT_BY_ID
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
    
    def get_patients_by_professional_id(self, professional_id: int) -> list[PacientList]:
        query = text(QUERY_GET_INFO_PATIENTS_BY_PROFESSIONAL_ID)
        result = self.db.execute(query, {"professional_id": professional_id}).fetchall()
        
        result_list = []
        
        for row in result:
            ano_actual = date.today().year
            edad = ano_actual - row.fechaNacimiento.year
            
            #Mapear
            paciente = PacientList(
                patient_id=row.pacienteId,
                name=row.nombre,
                last_name=row.apellidos,
                age = edad,
                photo=row.foto,
                glucose_level=row.nivelGlucosa,
                physical_activity_hours=row.horasActividadFisica,
                last_medication=row.medicamento,
                last_meal=row.comida,
                date=row.fecha
            )
            result_list.append(paciente)
        
        return result_list 
    
    def user_by_patient_id(self, patient_id: int) -> Usuario:
        query = text(QUERY_GET_USER_PATIENT_BY_ID)
        user = self.db.execute(query, {"patientId": patient_id}).first()
        return user
    
    def get_patient_by_id(self, id :int) -> PatientPlan:
        query = text(QUERY_GET_PATIENT_BY_ID)
        result = self.db.execute(query, {"id": id}).fetchone()
        
        #Mapear
        patient = PatientPlan(
            patient_id=result.pacienteId,
            full_name=result.fullName
        )
        return patient
    
    def get_patient_id_by_user_id(self, user_id: int) -> int:
        patient = self.db.query(Paciente).filter(Paciente.usuarioId == user_id).first()
        if patient.pacienteId != NOT_ID:
            return patient.pacienteId
        return None