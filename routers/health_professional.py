from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from requests import Session

from database.db import get_db
from services.health_professional import get_professional_id_by_user_id


router = APIRouter()

@router.get("/get_health_professional_id_by_user_id/{user_id}")
async def get_health_professional_id_by_user_id(user_id: int, db: Session = Depends(get_db)):
    health_professional_id = get_professional_id_by_user_id(db, user_id)
    if health_professional_id is 0:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "No se encontró el profesional."})
    return JSONResponse(status_code=status.HTTP_200_OK, content={"data": health_professional_id})