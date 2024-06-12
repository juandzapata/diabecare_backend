from datetime import date
from schemas.pdf import DataReportCreate
from data.models.base import Usuario
from exceptions.not_exists import NotExistsException
from services.pdf import PdfService
from fastapi import APIRouter, Depends, status, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from data.database.db import get_db
from schemas.patient import PatientList, PatientHistoryCreate, PatientHistoryRead, PatientPlan
from services.health_professional import HealthProfessionalService
from services.patient import PatientService
from sqlalchemy.orm import Session
from utils.constants.default_values import COUNT_ELEMENTS_ZERO


router = APIRouter()

@router.post("/create_patient_histories/", response_model=PatientHistoryRead, summary="Create patient history")
async def create_patient_history(history_create: PatientHistoryCreate, db: Session = Depends(get_db)):
    try:
        service = PatientService(db)
        patient_history = service.create_history(history_create)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"data": jsonable_encoder(patient_history),"statusCode": status.HTTP_201_CREATED, "message": "Historial creado."})
    except NotExistsException as e:
     return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR, "data":None, "message": e.get_message()})

@router.get("/patients_by_health_professional/{user_id}", response_model=list[PatientList], summary="Get patients by user id of a professional")
async def get_patients_by_professional(user_id: int, db: Session = Depends(get_db)):
    patient_service = PatientService(db)
    professional_service = HealthProfessionalService(db)
    
    try:
        professional = professional_service.get_professional_by_user_id(user_id)
        professional_id = professional.profesionalSaludId
        patients = patient_service.get_info_patients_by_professional_id(professional_id)
        if len(patients) > COUNT_ELEMENTS_ZERO:
            return JSONResponse(status_code=status.HTTP_200_OK, content={"data": jsonable_encoder(patients)})
        else:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "No se encontraron pacientes asignados al profesional"})
    except (NotExistsException) as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": e.get_message()})
    
@router.get("/patient_by_id/{id}", response_model=PatientPlan, summary="Get patient by patient id")
async def get_patient_by_id(id: int, db: Session = Depends(get_db)):
    service = PatientService(db)
    try:
        user_patient = service.get_user_patient_by_id(id)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"data": jsonable_encoder(user_patient)})
    except NotExistsException as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": e.get_message()})
   
@router.get("/generate_report/{patient_id}/{professional_user_id}", summary="Generate report", response_class=Response)
async def generate_pdf(patient_id: int, professional_user_id: int, db: Session = Depends(get_db)):
    data_report = DataReportCreate(patient_id=patient_id, professional_user_id=professional_user_id)
    service = PatientService(db)
    try:
        pdf_buffer = service.generate_pdf(data_report)
    except NotExistsException as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": e.get_message()})   
    
    date_created_str = date.today().strftime("%d-%m-%Y")
    headers = {
        "Content-Disposition": f"attachment; filename={'Reporte' + '-' + date_created_str}.pdf"
    }
    
    return Response(pdf_buffer.read(), media_type='application/pdf', headers=headers)