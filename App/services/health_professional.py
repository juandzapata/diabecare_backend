from services.patient import PatientService
from sqlalchemy import text
from data.models.base import ProfesionalSalud, Usuario
from schemas.patient import PacientList
from sqlalchemy.orm import Session
from utils.constants.default_values import NOT_ID, COUNT_ELEMENTS_ZERO



def get_professional_id_by_user_id(db: Session, usuario_id: int) -> int | None:
    result = db.query(ProfesionalSalud).filter(ProfesionalSalud.usuarioId == usuario_id).first()
    if result:
        return result.profesionalSaludId
    else:
        return None
    
def get_user_professional_by_id(professional_id: int, db) -> Usuario:
    professional = db.query(ProfesionalSalud).filter(ProfesionalSalud.profesionalSaludId == professional_id).first()
    user_professional = db.query(Usuario).filter(Usuario.usuarioId == professional.usuarioId).first()
    return user_professional
