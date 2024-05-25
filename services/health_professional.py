from sqlalchemy import text
from models.base import ProfesionalSalud
from schemas.patient import PacienteLista
from services.patient import get_info_patients_by_professional_id
from sqlalchemy.orm import Session


def get_patients(usuario_id: int, db) -> list[PacienteLista]:
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
    
