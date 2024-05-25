from pydantic import BaseModel
class NotificationMessage(BaseModel):
    name: str
    fullName: str
    title: str
    body: str
    deviceToken: str
