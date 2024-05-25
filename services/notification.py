import os
from fastapi import HTTPException
import httpx
from sqlalchemy import text

from schemas.notification import Notification, NotificationSend


def get_token_device_by_patient_id(db, patient_id: int) -> str:
    query = text("""
    SELECT tokenDispositivo
    FROM TokenUsuario T
    INNER JOIN Usuario U
    inner join Paciente P
                 on U.usuarioId = P.usuarioId
    ON T.usuarioId = U.usuarioId
    WHERE P.pacienteId = :patient_id
    """)
    result = db.execute(query, {"patient_id": patient_id}).fetchone()
    return result.tokenDispositivo

def send_notification(db, patient_id: int, title: str, body: str) -> None:
    token = get_token_device_by_patient_id(db, patient_id)
    url = os.getenv("MS-NOTIFICATION-URL")
    end_point = "/api/Notificación/EnviarNotificación"
    headers = {
        "Content-Type": "application/json"
    }
    notification : Notification = Notification(title=title, body=body)
    notification_send : NotificationSend = NotificationSend(registrationIds=[token], name="Nuevo plan personalizado", notification=notification, fullName="Nuevo plan personalizado")
    response = httpx.post(url+end_point, headers=headers, json=notification_send.dict())
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to send notification")
    

def save_token_device(db, patient_id: int, token: str) -> None:
    query = text("""
    INSERT INTO TokenUsuario (usuarioId, tokenDispositivo)
    SELECT U.usuarioId, :token
    FROM Usuario U
    inner join Paciente P
                 on U.usuarioId = P.usuarioId
    WHERE P.pacienteId = :patient_id
    """)
    db.execute(query, {"token": token, "patient_id": patient_id})
    db.commit()
    return None