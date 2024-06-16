from utils.mappers.user_mapper import UserMapper
from data.repositories.user_repository import UserRepository
from utils.exceptions.not_exists import NotExistsException
from utils.constants  import messages
from utils.constants.default_values import FIRST_ELEMENT_INDEX
from schemas.notification import NotificationMessage
from firebase_admin import messaging
from schemas.notification import tokenCreate, TokenDeviceOut
from services.recomendation import RecommendationService
from services.health_professional import HealthProfessionalService
from services.patient import PatientService
from data.models.base import TokenUsuario, Usuario
from schemas.personalized_planes import PersonalizedPlanCreate
from services.utils import convert_time_to_12_hour_format
class NotificationService:

    def __init__(self, db):
        self.db = db
        self.patient_service = PatientService(self.db)
        self.health_service = HealthProfessionalService(self.db)
        self.recommendation_service = RecommendationService(self.db)
        self.user_repository = UserRepository(self.db)

    def send_notification(self, plan: PersonalizedPlanCreate):
        """
        Sends a notification to the user associated with the given plan.

        Args:
            plan (PersonalizedPlanCreate): The personalized plan object.

        Returns:
            dict: A dictionary containing the result of the notification sending process.
                If successful, the dictionary will contain the notification details.
                If an error occurs, the dictionary will contain an "error" key with the error message.
        """
        user_patient = self.patient_service.get_user_patient_by_id(plan.pacienteId)
        user_patient_id = user_patient.usuarioId
        plan_id = plan.recomendaciones[FIRST_ELEMENT_INDEX].planId
        device_id = self.db.query(TokenUsuario).filter(TokenUsuario.usuarioId == user_patient_id).first().tokenDispositivo
        try:
            user_professional = self.health_service.get_user_professional_by_id(plan.profesionalSaludId)
            message = self.create_message(user_patient, user_professional, plan_id, device_id)
            return self.send_notification_user(message)
        except NotExistsException as e:
            return {"error": str(e.get_message())}

    def create_message(self, patient: Usuario, professional: Usuario, plan_id: int, device_id: str) -> NotificationMessage:
        """
        Creates a notification message for a patient based on a plan.

        Args:
            patient (Usuario): The patient for whom the message is created.
            professional (Usuario): The professional who created the plan.
            plan_id (int): The ID of the plan.
            device_id (str): The device ID to which the message will be sent.

        Returns:
            NotificationMessage: The created notification message.
        """
        INCREMENT = 1
        recommendations = self.recommendation_service.get_recommendations_by_plan_id(plan_id)
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

    def send_notification_user(self, message: NotificationMessage):
        """
        Sends a notification to a user.

        Args:
            message (NotificationMessage): The notification message object containing the title, body, and device token.

        Returns:
            dict: A dictionary containing the response of the notification sending process. If successful, the dictionary
            will have a "message" key with the value "Notification sent successfully" and a "response" key with the response
            from the messaging service. If an error occurs, the dictionary will have an "error" key with the error message.
        """
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


    def post_token(self, token: tokenCreate) -> TokenDeviceOut:
        existing_token = self.user_repository.get_toke_user_by_user_id(token.userId)

        if existing_token:
            existing_token.tokenDispositivo = token.token
            db_token = existing_token
        else:
            db_token = TokenUsuario(
                tokenDispositivo=token.token,
                usuarioId=token.userId
            )
            db_token = self.user_repository.create_token_user(db_token)
        
        self.db.commit()
        self.db.refresh(db_token)
        
        token_device_out = UserMapper.to_user_token_out(db_token)
        
        return token_device_out

    def exists_user_token (self, user_id: int, db) -> bool:
        return db.query(TokenUsuario).filter(TokenUsuario.usuarioId == user_id).first() is not None
