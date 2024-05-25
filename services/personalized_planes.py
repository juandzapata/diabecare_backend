from datetime import date
from fastapi import HTTPException
import httpx
from schemas.personalized_planes import PersonalizedPlanCreate, PersonalizedPlanOut
from sqlalchemy.orm import Session
from models.base import PlanesPersonalizados, ProfesionalPaciente
from services.recomendation import post_recomendation

def post_personalized_plan (plan: PersonalizedPlanCreate, database) -> PersonalizedPlanOut:
    profesionalPacienteId = get_professional_patient(plan.pacienteId, plan.profesionalSaludId, database)
    db_plan: PlanesPersonalizados = PlanesPersonalizados(
        profesionalPacienteId = profesionalPacienteId,
        fechaCreacion = date.today()
    )
    database.add(db_plan)
    database.commit()
    database.refresh(db_plan)
    
    create_recommendations_for_plan(plan, db_plan.planId, database)

    # Send notification to the created plan
    return db_plan.planId

def create_recommendations_for_plan (plan: PersonalizedPlanCreate, planId: int , database) -> None:
    for i in range(len(plan.recomendaciones)):
        plan.recomendaciones[i].planId = planId
        post_recomendation(plan.recomendaciones[i], database)

def get_professional_patient (pacienteId: int, profesionalSaludId: int, database) -> int:
    return database.query(ProfesionalPaciente).filter(ProfesionalPaciente.pacienteId == pacienteId, ProfesionalPaciente.profesionalId == profesionalSaludId).first().profesionalPacienteId

#Crea un método para enviar una notificación haciendo solicitud al microservicio de notificaciones
async def send_notification (plan: PersonalizedPlanCreate) -> None:
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