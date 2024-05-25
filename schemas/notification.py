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

class tokenDeviceOut(BaseModel):
    tokenUsuarioId: int

class NotificationMessage(BaseModel):
    title: str
    body: str
    deviceToken: str
