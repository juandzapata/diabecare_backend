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