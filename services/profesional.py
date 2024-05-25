from sqlalchemy import text
from models.base import ProfesionalSalud
from schemas.paciente import PacienteLista
from services.paciente import obtener_info_pacientes_por_profesional
from sqlalchemy.orm import Session


def obtener_pacientes(usuario_id: int, db) -> list[PacienteLista]:
    profesional_id = obtener_profesional_id_por_usuario_id(db, usuario_id)
    if profesional_id != 0:
        lista_pacientes = obtener_info_pacientes_por_profesional(db, profesional_id)
        if len(lista_pacientes) > 0:
            return lista_pacientes
    return None
    
def obtener_profesional_id_por_usuario_id(db: Session, usuario_id: int) -> int:

    result = db.query(ProfesionalSalud).filter(ProfesionalSalud.usuarioId == usuario_id).first()
    
    print(result)
    if result:
        return result.profesionalSaludId
    else:
        return 0
    
