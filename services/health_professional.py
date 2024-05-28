from sqlalchemy import text
from data.models.base import ProfesionalSalud, Usuario
from schemas.patient import PacientList
from services.patient import get_info_patients_by_professional_id
from sqlalchemy.orm import Session
from utils.constants.default_values import NOT_ID, COUNT_ELEMENTS_ZERO


def get_patients(user_id: int, db) -> list[PacientList]:
    professional_id = get_professional_id_by_user_id(db, user_id)
    if professional_id != NOT_ID:
        patient_list = get_info_patients_by_professional_id(db, professional_id)
        if len(patient_list) > COUNT_ELEMENTS_ZERO:
            return patient_list
    return []
    
def get_professional_id_by_user_id(db: Session, usuario_id: int) -> int:

    result = db.query(ProfesionalSalud).filter(ProfesionalSalud.usuarioId == usuario_id).first()
    
    print(result)
    if result:
        return result.profesionalSaludId
    else:
        return 0
    
def get_user_professional_by_id(professional_id: int, db) -> Usuario:
    professional = db.query(ProfesionalSalud).filter(ProfesionalSalud.profesionalSaludId == professional_id).first()
    user_professional = db.query(Usuario).filter(Usuario.usuarioId == professional.usuarioId).first()
    return user_professional
