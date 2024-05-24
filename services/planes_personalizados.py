from fastapi import HTTPException
import httpx
from schemas.planes_personalizados import PlanPersonalizadoCreate, PlanPersonalizadoOut
from sqlalchemy.orm import Session
from models.base import PlanesPersonalizados, Recomendacion
from services.recomendacion import post_recomendacion

def post_plan_personalizado (plan: PlanPersonalizadoCreate, database) -> PlanPersonalizadoOut:
    db_plan: PlanesPersonalizados = PlanesPersonalizados(
        pacienteId = plan.pacienteId,
        profesionalSaludId = plan.profesionalSaludId,
        fechaCreacion = plan.fechaCreacion
    )
    database.add(db_plan)
    database.commit()
    database.refresh(db_plan)
    
    for i in range(len(plan.recomendaciones)):
        plan.recomendaciones[i].planId = db_plan.planId
        post_recomendacion(plan.recomendaciones[i], database)
    
    # Send notification to the created plan
    return PlanPersonalizadoOut(**db_plan.__dict__)

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