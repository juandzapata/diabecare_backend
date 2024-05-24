from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.db import get_db
from schemas.recomendacion import RecomendacionCreate, RecomendacionOut 
from services.recomendacion import post_recomendacion
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter()

@router.post("/recomendacion", summary="Crear una recomendación")
async def create_recomendacion(recomendacion: RecomendacionCreate, db: Session = Depends(get_db)):
    recomendacion_creada = post_recomendacion(recomendacion, db)
    if recomendacion_creada is None:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = f'Recomendacion is not added to the database'
        )
    return JSONResponse(
        status_code = status.HTTP_201_CREATED,
        content = {'data': recomendacion_creada}
   )