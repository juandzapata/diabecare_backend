
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from database.db import get_db
from schemas.personalized_planes import PersonalizedPlanCreate, PersonalizedPlanOut
from sqlalchemy.orm import Session
from services.personalized_planes import post_personalized_plan

router = APIRouter()
@router.post("/planes_personalizados", summary="Create a personalized plan")
async def create_plan_personalizado(plan: PersonalizedPlanCreate, db: Session = Depends(get_db)):
    plan_creado = post_personalized_plan(plan, db)
    if plan_creado is None:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = f'Plan personalizado is not added to the database'
        )
    return JSONResponse( 
        status_code = status.HTTP_201_CREATED,
        content = {'data': plan_creado}
    )