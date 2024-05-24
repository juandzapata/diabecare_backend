from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from database.db import get_db
from schemas.paciente import PacienteLista
from services.profesional import obtener_pacientes
from sqlalchemy.orm import Session


router = APIRouter()

@router.get("/pacientes_por_profesional/{user_id}", response_model=list[PacienteLista], summary="Obtener los pacientes asignados a un profesional especifico")
async def obtener_pacientes_por_profesional(user_id: int, db: Session = Depends(get_db)):
    print(user_id)
    pacientes = obtener_pacientes(user_id, db)
    print(pacientes)
    if pacientes is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Este profesional no tiene pacientes asignados."})
    return JSONResponse(status_code=status.HTTP_200_OK, content={"data": jsonable_encoder(pacientes)})
    