
from utils.exceptions.not_exists import NotExistsException
from utils.constants.default_values import COUNT_ELEMENTS_ZERO
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from data.database.db import get_db
from schemas.personalized_planes import PersonalizedPlanCreate
from sqlalchemy.orm import Session
from services.personalized_planes import PersonalizedPlanesService

router = APIRouter()
@router.post("/planes_personalizados", summary="Create a personalized plan")
async def create_plan_personalizado(plan: PersonalizedPlanCreate, db: Session = Depends(get_db)):
    service = PersonalizedPlanesService(db)
    
    try:
        plan_created = service.post_personalized_plan(plan)
        print("plan_created", plan_created)
        return JSONResponse(status_code = status.HTTP_200_OK, content = {'data': jsonable_encoder(plan_created)})
    except NotExistsException as e:
        return JSONResponse(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, content = {'message': e.get_message()})
        
@router.get("/planes_personalizados/{user_id}", summary="Get personalized plans by user id")
async def get_personalized_planes_by_user_id(user_id: int, db: Session = Depends(get_db)):
    service = PersonalizedPlanesService(db)
    try:
        planes = service.get_planes_by_user_id(user_id)
        if len(planes) > COUNT_ELEMENTS_ZERO:
            return JSONResponse(status_code = status.HTTP_200_OK, content = {'data': jsonable_encoder(planes)})
        else:
            return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content = {'message': 'No se encontraron planes'})
    except NotExistsException as e:
         return JSONResponse(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, content = {'message': e.get_message()})