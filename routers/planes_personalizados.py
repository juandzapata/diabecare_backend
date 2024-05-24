
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from database.db import get_db
from schemas.planes_personalizados import PlanPersonalizadoCreate, PlanPersonalizadoOut
from sqlalchemy.orm import Session
from services.planes_personalizados import post_plan_personalizado

router = APIRouter()
@router.post("/planes_personalizados", response_model=PlanPersonalizadoOut, summary="Crear un plan personalizado")
async def create_plan_personalizado(plan: PlanPersonalizadoCreate, db: Session = Depends(get_db)) -> PlanPersonalizadoOut:
    print( "La información que llega del plan es: ", plan.__dict__)
    plan_creado: PlanPersonalizadoOut = post_plan_personalizado(plan, db)
    if plan_creado is None:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = f'Plan personalizado {plan.titulo} is not added to the database'
        )
    return JSONResponse( 
        status_code = status.HTTP_201_CREATED,
        content = {'data': plan_creado}
    )