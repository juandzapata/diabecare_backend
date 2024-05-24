from schemas.recomendacion import RecomendacionCreate, RecomendacionOut
from sqlalchemy.orm import Session
from models.base import Recomendacion

def post_recomendacion (recomendacion: RecomendacionCreate, database: Session) -> RecomendacionOut:
    db_recomendacion: Recomendacion = Recomendacion(**recomendacion.model_dump())
    database.add(db_recomendacion)
    database.commit()
    database.refresh(db_recomendacion)
    return db_recomendacion.recomendacionId