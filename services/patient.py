from datetime import date
from data.repositories.patient_repository import PatientRepository
from utils.constants.query import QUERY_GET_INFO_PATIENTS_BY_PROFESSIONAL_ID, QUERY_GET_PATIENT_BY_ID, QUERY_GET_USER_PATIENT_BY_ID 
from data.models.base import HistorialDatos, ProfesionalPaciente, Usuario, ProfesionalSalud
from sqlalchemy import text
from data.models.base import Paciente
from schemas.patient import PacientList, PatientHistoryCreate, PatientHistoryRead, PatientPlan



def create_history(history_create: PatientHistoryCreate, db) -> PatientHistoryRead:
    repository = PatientRepository(db)
    history = HistorialDatos(**history_create.dict())
    created_history = repository.create(history)
    return PatientHistoryRead.from_orm(created_history)


def get_info_patients_by_professional_id(db, professional_id: int) -> list[PacientList]:
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

def get_user_patient_by_id(id: int, db) -> Usuario:
    query = text(QUERY_GET_USER_PATIENT_BY_ID)
    user = db.execute(query, {"patientId": id}).first()
    return user

def get_patient(id :int, db) -> PatientPlan:
    query = text(QUERY_GET_PATIENT_BY_ID)
    result = db.execute(query, {"id": id}).fetchone()
    patient = PatientPlan(
        patient_id=result.pacienteId,
        full_name=result.fullName
    )
    return patient