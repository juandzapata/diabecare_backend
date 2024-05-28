from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from data.database.db import get_db
from schemas.patient import PacientList, PatientPlan
from services.health_professional import get_patients
from sqlalchemy.orm import Session
from services.patient import get_patient


router = APIRouter()

@router.get("/patients_by_health_professional/{user_id}", response_model=list[PacientList], summary="Get patients by user id of a professional")
async def get_patients_by_professional(user_id: int, db: Session = Depends(get_db)):
    print(user_id)
    pacientes = get_patients(user_id, db)
    print(pacientes)
    if pacientes is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Este profesional no tiene pacientes asignados."})
    return JSONResponse(status_code=status.HTTP_200_OK, content={"data": jsonable_encoder(pacientes)})

@router.get("/patient_by_id/{id}", response_model=PatientPlan, summary="Get patient by user id")
async def get_patient_by_id(id: int, db: Session = Depends(get_db)):
    patient = get_patient(id, db)
    if patient is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "No se encontró el paciente."})
    return JSONResponse(status_code=status.HTTP_200_OK, content={"data": jsonable_encoder(patient)})