from datetime import date
from constants.query import QUERY_GET_INFO_PATIENTS_BY_PROFESSIONAL_ID, QUERY_GET_USER_PATIENT_BY_ID 

from models.base import ProfesionalPaciente, Usuario, ProfesionalSalud
from sqlalchemy import text
from schemas.patient import PacientList
def get_info_patients_by_professional_id(db, professional_id: int) -> list[PacientList]:
    print(professional_id)
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

def get_professional_by_patient_id(patient_id: int, db) -> Usuario:
    professional_id = db.query(ProfesionalPaciente).filter(ProfesionalPaciente.pacienteId == patient_id).first().profesionalId
    professional = db.query(ProfesionalSalud).filter(ProfesionalSalud.profesionalSaludId == professional_id).first()
    user_professional = db.query(Usuario).filter(Usuario.usuarioId == professional.usuarioId).first()
    return user_professional
