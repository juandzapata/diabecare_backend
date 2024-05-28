from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from data.database.db import get_db
from schemas.patient import PacientList, PatientHistoryCreate, PatientHistoryRead, PatientPlan
from services.health_professional import get_patients
from sqlalchemy.orm import Session
from services.patient import get_patient
from services import patient
from utils.constants.default_values import COUNT_ELEMENTS_ZERO


router = APIRouter()

@router.post("/create_patient_histories/", response_model=PatientHistoryRead, summary="Create patient history")
async def create_patient_history(history_create: PatientHistoryCreate, db: Session = Depends(get_db)):
    patient_history = patient.create_history(history_create, db)
    if patient_history is not None:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"data": jsonable_encoder(patient_history)})
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "No se pudo crear el historial."})

@router.get("/patients_by_health_professional/{user_id}", response_model=list[PacientList], summary="Get patients by user id of a professional")
async def get_patients_by_professional(user_id: int, db: Session = Depends(get_db)):
    patients = get_patients(user_id, db)
    if len(patients) == COUNT_ELEMENTS_ZERO:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Este profesional no tiene pacientes asignados."})
    return JSONResponse(status_code=status.HTTP_200_OK, content={"data": jsonable_encoder(patients)})

@router.get("/patient_by_id/{id}", response_model=PatientPlan, summary="Get patient by user id")
async def get_patient_by_id(id: int, db: Session = Depends(get_db)):
    patient = get_patient(id, db)
    if patient is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "No se encontró el paciente."})
    return JSONResponse(status_code=status.HTTP_200_OK, content={"data": jsonable_encoder(patient)})