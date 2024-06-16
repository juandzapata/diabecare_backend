from utils.exceptions.not_created import NotCreatedException
from utils.constants.default_values import COUNT_ELEMENTS_ZERO
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from data.database.db import get_db
from schemas.recommendation import RecommendationCreate, RecommendationOut
from services.recomendation import RecommendationService
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter()

@router.post("/recommendation", summary="Create a recommendation")
async def create_recomendation(recommendation: RecommendationCreate, db: Session = Depends(get_db)):
    service = RecommendationService(db)
    try:
        recommendation_create = service.post_recommendation(recommendation, db)
        return JSONResponse(status_code = status.HTTP_200_OK, content = {'data': jsonable_encoder(recommendation_create)})
    except NotCreatedException as e:
        return JSONResponse(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, content = {'message': e.get_message()})
    
@router.get("/recommendations/{plan_id}", summary="Get recomendations by plan id")
async def get_recommendations_by_plan_id(plan_id: int, db: Session = Depends(get_db)):
    service = RecommendationService(db)
    recomendations = service.get_recommendations_by_plan_id(plan_id)
    if len(recomendations) > COUNT_ELEMENTS_ZERO:
        return JSONResponse(status_code = status.HTTP_200_OK, content = {'data': jsonable_encoder(recomendations)})
    return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content = {'message': 'No recommendations found'})