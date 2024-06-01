from utils.constants  import messages
from utils.constants.default_values import FIRST_ELEMENT_INDEX
from schemas.notification import NotificationMessage
from firebase_admin import messaging
from schemas.notification import tokenCreate, TokenDeviceOut
from services import recomendation as recomendationService
from services import patient, health_professional
from data.models.base import TokenUsuario, Usuario
from schemas.personalized_planes import PersonalizedPlanCreate
from services.utils import convert_time_to_12_hour_format

class NotificationService:
    def __init__(self, db):
        self.db = db
    def send_notification (self, plan: PersonalizedPlanCreate):
        user_patient = patient.get_user_patient_by_id(plan.pacienteId, self.db)
        user_patient_id = user_patient[FIRST_ELEMENT_INDEX]
        plan_id = plan.recomendaciones[FIRST_ELEMENT_INDEX].planId
        device_id = self.db.query(TokenUsuario).filter(TokenUsuario.usuarioId == user_patient_id).first().tokenDispositivo
        user_professional = health_professional.get_user_professional_by_id(plan.profesionalSaludId, self.db)
        message = self.create_message(user_patient, user_professional, plan_id , device_id)
        return self.send_notification_user(message)

    def create_message(self, patient: Usuario, professional: Usuario, plan_id: int, device_id: str) -> NotificationMessage:
        INCREMENT = 1
        recommendations = recomendationService.get_recommendations_by_plan_id(plan_id, self.db)
        hora = convert_time_to_12_hour_format(recommendations[FIRST_ELEMENT_INDEX].horaEjecucion)
        print("Horaaaa", hora)
        message = f"Hola {patient.nombre}!. El Dr. {professional.nombre} te creo un nuevo plan con las siguientes recomendaciones: \n"
        for recommendation_index in range(len(recommendations)):
            hora = convert_time_to_12_hour_format(recommendations[recommendation_index].horaEjecucion)
            print("Horaaaa", hora)
            message += f" {recommendation_index + INCREMENT}. {recommendations[recommendation_index].titulo} - Hora: {hora}. \n"
        message = NotificationMessage(
            title = messages.CREATE_PLAN,
            body = message,
            deviceToken = device_id
        )
        return message

    def send_notification_user(self, message:NotificationMessage):
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


    def post_token(self, token: tokenCreate, database) -> TokenDeviceOut:
        existing_token = database.query(TokenUsuario).filter_by(usuarioId=token.userId).first()

        if existing_token:
            existing_token.tokenDispositivo = token.token
            db_token = existing_token
        else:
            db_token = TokenUsuario(
                tokenDispositivo=token.token,
                usuarioId=token.userId
            )
            database.add(db_token)
        
        database.commit()
        database.refresh(db_token)
        
        token_device_out = TokenDeviceOut(
            usuarioId=db_token.usuarioId,
            tokenDispositivo=db_token.tokenDispositivo,
            tokenUsuarioId=db_token.tokenUsuarioId
        )
        
        return token_device_out

    def exists_user_token (self, user_id: int, db) -> bool:
        return db.query(TokenUsuario).filter(TokenUsuario.usuarioId == user_id).first() is not None
