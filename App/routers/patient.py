from datetime import date
from services.pdf import PdfService
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from data.database.db import get_db
from schemas.patient import PacientList, PatientHistoryCreate, PatientHistoryRead, PatientPlan
from services.health_professional import HealthProfessionalService
from services.patient import PatientService
from sqlalchemy.orm import Session
from utils.constants.default_values import COUNT_ELEMENTS_ZERO


router = APIRouter()

@router.post("/create_patient_histories/", response_model=PatientHistoryRead, summary="Create patient history")
async def create_patient_history(history_create: PatientHistoryCreate, db: Session = Depends(get_db)):
    service = PatientService(db)
    patient_history = service.create_history(history_create)
    if patient_history is not None:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"data": jsonable_encoder(patient_history)})
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "No se pudo crear el historial."})

@router.get("/patients_by_health_professional/{user_id}", response_model=list[PacientList], summary="Get patients by user id of a professional")
async def get_patients_by_professional(user_id: int, db: Session = Depends(get_db)):
    patient_service = PatientService(db)
    professional_service = HealthProfessionalService(db)
    professional_id = professional_service.get_professional_id_by_user_id(user_id)
    patients = patient_service.get_info_patients_by_professional_id(professional_id)
    if len(patients) == COUNT_ELEMENTS_ZERO:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Este profesional no tiene pacientes asignados."})
    return JSONResponse(status_code=status.HTTP_200_OK, content={"data": jsonable_encoder(patients)})

@router.get("/patient_by_id/{id}", response_model=PatientPlan, summary="Get patient by patient id")
async def get_patient_by_id(id: int, db: Session = Depends(get_db)):
    service = PatientService(db)
    patient = service.get_patient(id)
    if patient is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "No se encontró el paciente."})
    return JSONResponse(status_code=status.HTTP_200_OK, content={"data": jsonable_encoder(patient)})

@router.get("/generate_report/{patient_id}", summary="Generate report", response_class=Response)
async def generate_pdf(patient_id: int, db: Session = Depends(get_db)):
    service = PatientService(db)
    patient = service.get_data_report(patient_id)
    if patient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontró el paciente.")
    
    service_pdf = PdfService()
    pdf_buffer = service_pdf.generate_pdf(patient)
    date_created_str = date.today().strftime("%d-%m-%Y")
    headers = {
        "Content-Disposition": f"attachment; filename={'Reporte-' + patient.full_name + '-' + date_created_str}.pdf"
    }
    
    return Response(pdf_buffer.read(), media_type='application/pdf', headers=headers)