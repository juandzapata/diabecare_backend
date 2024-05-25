from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.db import get_db
from schemas.recomendation import RecomendationCreate, RecomendationOut 
from services.recomendation import post_recomendation
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter()

@router.post("/recomendation", summary="Create a recomendation")
async def create_recomendation(recomendation: RecomendationCreate, db: Session = Depends(get_db)):
    recomendacion_creada = post_recomendation(recomendation, db)
    if recomendacion_creada is None:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = f'Recomendacion is not added to the database'
        )
    return JSONResponse(
        status_code = status.HTTP_201_CREATED,
        content = {'data': recomendacion_creada}
   )