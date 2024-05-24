from datetime import date
from fastapi import HTTPException
import httpx
from schemas.planes_personalizados import PlanPersonalizadoCreate, PlanPersonalizadoOut
from sqlalchemy.orm import Session
from models.base import PlanesPersonalizados, ProfesionalPaciente
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
async def send_notification (plan: PlanPersonalizadoCreate) -> None:
    # Datos de la notificación que quieres enviar
    notification_data = {
        "planId": plan.planId,
        "userId": plan.userId,
        "message": "Un nuevo plan personalizado ha sido creado."
    }

    # URL del microservicio .NET
    notification_url = "http://mi-microservicio-net/api/notificaciones"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(notification_url, json=notification_data)
            response.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=response.status_code, detail=f"Error enviando la notificación: {e.response.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error enviando la notificación: {str(e)}")