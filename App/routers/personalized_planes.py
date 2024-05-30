
from utils.constants.default_values import COUNT_ELEMENTS_ZERO
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from data.database.db import get_db
from schemas.personalized_planes import PersonalizedPlanCreate, PersonalizedPlanOut
from sqlalchemy.orm import Session
from services.personalized_planes import PersonalizedPlanesService

router = APIRouter()
@router.post("/planes_personalizados", summary="Create a personalized plan")
async def create_plan_personalizado(plan: PersonalizedPlanCreate, db: Session = Depends(get_db)):
    service = PersonalizedPlanesService(db)
    plan_creado = service.post_personalized_plan(plan)
    if plan_creado is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = f'No puedes crear un plan para un paciente que no tienes asignado'
        )
    return JSONResponse( 
        status_code = status.HTTP_201_CREATED,
        content = {'data': plan_creado}
    )

@router.get("/planes_personalizados/{user_id}", summary="Get personalized plans by user id")
async def get_personalized_planes_by_user_id(user_id: int, db: Session = Depends(get_db)):
    service = PersonalizedPlanesService(db)
    planes = service.get_planes_by_user_id(user_id)
    if len(planes) > COUNT_ELEMENTS_ZERO:
        return JSONResponse(status_code = status.HTTP_200_OK, content = {'data': jsonable_encoder(planes)})
    return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content = {'message': 'No se encontraton planes'})