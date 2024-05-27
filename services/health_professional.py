from sqlalchemy import text
from models.base import ProfesionalSalud, Usuario
from schemas.patient import PacientList
from services.patient import get_info_patients_by_professional_id
from sqlalchemy.orm import Session


def get_patients(usuario_id: int, db) -> list[PacientList]:
    profesional_id = get_professional_id_by_user_id(db, usuario_id)
    if profesional_id != 0:
        lista_pacientes = get_info_patients_by_professional_id(db, profesional_id)
        if len(lista_pacientes) > 0:
            return lista_pacientes
    return None
    
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
