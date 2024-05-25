from typing import List
from pydantic import BaseModel

class Notification(BaseModel):
    title: str
    body: str

class NotificationSend(BaseModel):
    registrationIds: List[str]
    name: str
    notification: Notification
    fullName: str

class tokenCreate(BaseModel):
    token: str
    userId: int

class TokenDeviceOut(BaseModel):
    usuarioId: int
    tokenDispositivo: str
    tokenUsuarioId: int

    def model_dump(self):
        return {
            "usuarioId": self.usuarioId,
            "tokenDispositivo": self.tokenDispositivo,
            "tokenUsuarioId": self.tokenUsuarioId
        }

class NotificationMessage(BaseModel):
    title: str
    body: str
    deviceToken: str
