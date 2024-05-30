from datetime import date, datetime
from data.repositories.patient_repository import PatientRepository
from utils.constants.default_values import COUNT_ELEMENTS_ZERO, NOT_ID
from utils.constants.query import QUERY_GET_INFO_PATIENTS_BY_PROFESSIONAL_ID, QUERY_GET_PATIENT_BY_ID, QUERY_GET_USER_PATIENT_BY_ID 
from data.models.base import HistorialDatos, Usuario 
from sqlalchemy import text
from schemas.patient import PacientList, PatientHistoryCreate, PatientHistoryRead, PatientPlan


class PatientService:
    def __init__(self, db):
        self.patient_repository = PatientRepository(db)

    def create_history(self, history_create: PatientHistoryCreate) -> PatientHistoryRead:
        history = HistorialDatos(**history_create.__dict__)
        history.fecha = datetime.today()
        created_history =  self.patient_repository.create(history)
        return PatientHistoryRead.model_validate(created_history)


    def get_info_patients_by_professional_id(self, professional_id: int, db) -> list[PacientList]:
        query = text(QUERY_GET_INFO_PATIENTS_BY_PROFESSIONAL_ID)
        result = db.execute(query, {"profesional_id": professional_id}).fetchall()
        
        result_list = []
        
        for row in result:
            ano_actual = date.today().year
            edad = ano_actual - row.fechaNacimiento.year
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

    def get_user_patient_by_id(self, id: int, db) -> Usuario:
        query = text(QUERY_GET_USER_PATIENT_BY_ID)
        user = db.execute(query, {"patientId": id}).first()
        return user

    def get_patient(self, id :int, db) -> PatientPlan:
        query = text(QUERY_GET_PATIENT_BY_ID)
        result = db.execute(query, {"id": id}).fetchone()
        patient = PatientPlan(
            patient_id=result.pacienteId,
            full_name=result.fullName
        )
        return patient
    def get_patients_by_professional_id(self, professional_id: int, db) -> list[PacientList]:
        service = PatientService(db)
        if professional_id != NOT_ID:
            patient_list = service.get_info_patients_by_professional_id(professional_id, db)
            if len(patient_list) > COUNT_ELEMENTS_ZERO:
                return patient_list
        return []
    