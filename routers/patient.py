from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from database.db import get_db
from schemas.patient import PacienteLista
from services.health_professional import get_patients
from sqlalchemy.orm import Session


router = APIRouter()

@router.get("/patients_by_health_professional/{user_id}", response_model=list[PacienteLista], summary="Get patients by user id of a professional")
async def get_patients_by_professional(user_id: int, db: Session = Depends(get_db)):
    print(user_id)
    pacientes = get_patients(user_id, db)
    print(pacientes)
    if pacientes is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Este profesional no tiene pacientes asignados."})
    return JSONResponse(status_code=status.HTTP_200_OK, content={"data": jsonable_encoder(pacientes)})
    