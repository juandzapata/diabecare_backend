from exceptions.not_exists import NotExistsException
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from requests import Session

from data.database.db import get_db
from services.health_professional import HealthProfessionalService


router = APIRouter()

@router.get("/get_health_professional_id_by_user_id/{user_id}")
async def get_health_professional_id_by_user_id(user_id: int, db: Session = Depends(get_db)):
    service = HealthProfessionalService(db)
    try: 
        health_professional = service.get_professional_by_user_id(user_id)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"data": jsonable_encoder(health_professional)})
    except NotExistsException as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": e.get_message()}) 
