from datetime import date
import os
from fastapi import HTTPException
import httpx
from sqlalchemy import text
from schemas.planes_personalizados import PlanPersonalizadoCreate, PlanPersonalizadoOut
from sqlalchemy.orm import Session
from models.base import PlanesPersonalizados, ProfesionalPaciente
from services.notification import send_notification
from services.recomendacion import post_recomendacion

def post_plan_personalizado (plan: PlanPersonalizadoCreate, database) -> PlanPersonalizadoOut:
    profesionalPacienteId = buscar_ProfecionalPaciente(plan.pacienteId, plan.profesionalSaludId, database)
    db_plan: PlanesPersonalizados = PlanesPersonalizados(
        profesionalPacienteId = profesionalPacienteId,
        fechaCreacion = date.today()
    )
    database.add(db_plan)
    database.commit()
    database.refresh(db_plan)
    
    crear_recomendaciones_plan(plan, db_plan.planId, database)
    # Send notification to the created plan
    return db_plan.planId

def crear_recomendaciones_plan (plan: PlanPersonalizadoCreate, planId: int , database) -> None:
    for i in range(len(plan.recomendaciones)):
        plan.recomendaciones[i].planId = planId
        post_recomendacion(plan.recomendaciones[i], database)

def buscar_ProfecionalPaciente (pacienteId: int, profesionalSaludId: int, database) -> int:
    return database.query(ProfesionalPaciente).filter(ProfesionalPaciente.pacienteId == pacienteId, ProfesionalPaciente.profesionalId == profesionalSaludId).first().profesionalPacienteId


#Crea un método para enviar una notificación haciendo solicitud al microservicio de notificaciones
async def send_notification_plan (db, plan: PlanPersonalizadoCreate) -> None:
    return await send_notification(db, plan.pacienteId, "Nuevo plan personalizado", "Se ha creado un nuevo plan personalizado para ti")