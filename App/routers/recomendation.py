from utils.constants.default_values import COUNT_ELEMENTS_ZERO
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from data.database.db import get_db
from schemas.recomendation import RecomendationCreate, RecomendationOut 
from services.recomendation import RecommendationService
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter()

@router.post("/recomendation", summary="Create a recomendation")
async def create_recomendation(recomendation: RecomendationCreate, db: Session = Depends(get_db)):
    service = RecommendationService(db)
    recomendacion_creada = service.post_recommendation(recomendation, db)
    if recomendacion_creada is None:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = f'Recomendacion is not added to the database'
        )
    return JSONResponse(
        status_code = status.HTTP_201_CREATED,
        content = {'data': recomendacion_creada}
   )
    
@router.get("/recomendations/{plan_id}", summary="Get recomendations by plan id")
async def get_recommendations_by_plan_id(plan_id: int, db: Session = Depends(get_db)):
    service = RecommendationService(db)
    recomendations = service.get_recommendations_by_plan_id(plan_id)
    if len(recomendations) > COUNT_ELEMENTS_ZERO:
        return JSONResponse(status_code = status.HTTP_200_OK, content = {'data': jsonable_encoder(recomendations)})
    return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content = {'message': 'No recomendations found'})