from constants  import messages
from constants.default_values import FIRST_ELEMENT_INDEX
from schemas.notification import NotificationMessage
from firebase_admin import messaging
from schemas.notification import tokenCreate, tokenDeviceOut
from services import recomendation as recomendationService
from services import patient
from models.base import TokenUsuario, Usuario
from schemas.personalized_planes import PersonalizedPlanCreate


def send_notification (plan: PersonalizedPlanCreate, db):
    user_patient = patient.get_user_patient_by_id(plan.pacienteId, db)
    user_patient_id = user_patient[FIRST_ELEMENT_INDEX]
    plan_id = plan.recomendaciones[FIRST_ELEMENT_INDEX].planId
    device_id = db.query(TokenUsuario).filter(TokenUsuario.usuarioId == user_patient_id).first().tokenDispositivo
    user_professional = patient.get_professional_by_patient_id(plan.pacienteId, db)
    message = create_message(user_patient, user_professional, plan_id , device_id, db)
    return send_notification_user(message)

def create_message(patient: Usuario, professioanl: Usuario, planId: int, deviceId: str, db) -> NotificationMessage:
    INCREMENT = 1
    recomendations = recomendationService.get_recomendarions_by_plan_id(planId, db)
    message = f"Hola {patient.nombre}!. El Dr. {professioanl.nombre} te creo un nuevo plan con las siguientes recomendaciones: \n"
    for recomendation_index in range(len(recomendations)):
        message += f" {recomendation_index + INCREMENT}.  {recomendations[recomendation_index].titulo}. \n"
    message = NotificationMessage(
        title = messages.CREATE_PLAN,
        body = message,
        deviceToken = deviceId
    )
    return message

def send_notification_user(message:NotificationMessage):
    try:
        notification = messaging.Notification(
            title=message.title,
            body=message.body
        )
        message = messaging.Message(
            notification=notification,
            token=message.deviceToken
        )
        response = messaging.send(message)
        return {"message": "Notification sent successfully", "response": response}
    except Exception as ex:
        return {"error": str(ex)}


def post_token (token: tokenCreate, database) -> tokenDeviceOut:

    db_token : TokenUsuario = TokenUsuario(
        tokenDispositivo = token.token,
        usuarioId = token.userId
    )
    if exists_user_token(token.userId, database):
        database.update(db_token)
    else:
        database.add(db_token)
    database.commit()
    database.refresh(db_token)
    return db_token.tokenUsuarioId

def exists_user_token (userId: int, db) -> bool:
    return db.query(TokenUsuario).filter(TokenUsuario.usuarioId == userId).first() is not None
