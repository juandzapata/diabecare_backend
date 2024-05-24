
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from database.db import get_db
from schemas.planes_personalizados import PlanPersonalizadoCreate, PlanPersonalizadoOut
from sqlalchemy.orm import Session
from services.planes_personalizados import post_plan_personalizado

router = APIRouter()
@router.post("/planes_personalizados", summary="Crear un plan personalizado")
async def create_plan_personalizado(plan: PlanPersonalizadoCreate, db: Session = Depends(get_db)):
    plan_creado = post_plan_personalizado(plan, db)
    if plan_creado is None:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = f'Plan personalizado is not added to the database'
        )
    return JSONResponse( 
        status_code = status.HTTP_201_CREATED,
        content = {'data': plan_creado}
    )