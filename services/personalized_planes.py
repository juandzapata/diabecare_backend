from datetime import date
from constants.messages import CREATE_PLAN
from fastapi import HTTPException
from schemas.notification import NotificationMessage
from schemas.personalized_planes import PersonalizedPlanCreate, PersonalizedPlanOut
from models.base import PlanesPersonalizados, ProfesionalPaciente, TokenUsuario
from services import recomendation, notification

def post_personalized_plan (plan: PersonalizedPlanCreate, database) -> PersonalizedPlanOut:
    profesionalPaciente = get_professional_patient(plan.pacienteId, plan.profesionalSaludId, database)
    db_plan: PlanesPersonalizados = PlanesPersonalizados(
        profesionalPacienteId = profesionalPaciente.profesionalPacienteId,
        fechaCreacion = date.today()
    )
    database.add(db_plan)
    database.commit()
    database.refresh(db_plan)
    
    create_recommendations_for_plan(plan, db_plan.planId, database)

    # Send notification to the created plan
    notification.send_notification(plan, database)
    return db_plan.planId

def create_recommendations_for_plan (plan: PersonalizedPlanCreate, planId: int , database) -> None:
    for i in range(len(plan.recomendaciones)):
        plan.recomendaciones[i].planId = planId
        recomendation.post_recomendation(plan.recomendaciones[i], database)

def get_professional_patient (pacienteId: int, profesionalSaludId: int, database) -> ProfesionalPaciente:
    return database.query(ProfesionalPaciente).filter(ProfesionalPaciente.pacienteId == pacienteId, ProfesionalPaciente.profesionalId == profesionalSaludId).first()




