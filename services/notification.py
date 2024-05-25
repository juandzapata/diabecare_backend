from constants  import messages
from schemas.notification import NotificationMessage
from firebase_admin import messaging
from schemas.notification import tokenCreate, tokenDeviceOut
from services import recomendation as recomendationService
from services import patient
from models.base import TokenUsuario, Usuario
from schemas.personalized_planes import PersonalizedPlanCreate


def send_notification (plan: PersonalizedPlanCreate, db):
    userPatient = patient.get_user_patient_by_id(plan.pacienteId, db)
    deviceId = db.query(TokenUsuario).filter(TokenUsuario.usuarioId == userPatient[0]).first().tokenDispositivo
    message = create_message(userPatient, plan.recomendaciones[0].planId, deviceId, db)
    return send_notification_user(message, db)

def create_message(patient: Usuario, planId: int, deviceId: str, db) -> NotificationMessage:
    recomendations = recomendationService.get_recomendarions_by_plan_id(planId, db)
    message = f"Hola {patient.nombre}!. se te creo un nuevo plan las recomendaciones del plan son: "
    for recomendation in recomendations:
        message += f"{recomendation.titulo}. "
    message = NotificationMessage(
        title = messages.CREATE_PLAN,
        body = message,
        deviceToken = deviceId
    )
    return message

def send_notification_user(message:NotificationMessage, db):
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
