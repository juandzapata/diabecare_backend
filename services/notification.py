from schemas.message import NotificationMessage
from firebase_admin import messaging


async def send_notification_user(message:NotificationMessage, db):
    try:
        notification = messaging.Notification(
            title=message.title,
            body=message.body
        )
        message = messaging.Message(
            notification=notification,
            data={
                "FirstName": message.name,
                "LastName": message.fullName
            },
            token=message.deviceToken
        )
        response = messaging.send(message)
        return {"message": "Notification sent successfully", "response": response}
    except Exception as ex:
        return {"error": str(ex)}
