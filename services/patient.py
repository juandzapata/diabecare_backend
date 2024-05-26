from datetime import date
from constants.query import QUERY_GET_INFO_PATIENTS_BY_PROFESSIONAL_ID, QUERY_GET_PATIENT_BY_ID 

from sqlalchemy import text
from models.base import Paciente
from schemas.patient import PacienteLista, PatientPlan
def get_info_patients_by_professional_id(db, profesional_id: int) -> list[PacienteLista]:
    query = text(QUERY_GET_INFO_PATIENTS_BY_PROFESSIONAL_ID)
    result = db.execute(query, {"profesional_id": profesional_id}).fetchall()
    
    result_list = []
    
    for row in result:
        ano_actual = date.today().year
        edad = ano_actual - row.fechaNacimiento.year
        paciente = PacienteLista(
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

def get_patient(id :int, db) -> PatientPlan:
    query = text(QUERY_GET_PATIENT_BY_ID)
    result = db.execute(query, {"id": id}).fetchone()
    patient = PatientPlan(
        patient_id=result.pacienteId,
        full_name=result.fullName
    )
    return patient