from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from database.db import get_db
from schemas.message import NotificationMessage
from sqlalchemy.orm import Session
from services import notification



router = APIRouter()
@router.post('/send_notification', summary='Send a notification to a user.')
async def send_notification(message: NotificationMessage, db: Session = Depends(get_db)):
    token = await notification.send_notification_user(message, db)
    if token is None:
        return JSONResponse(status_code=404, content={"message": "Usuario no se encontro"})
    return JSONResponse(status_code=200, content={"token": token, "statusCode": 200})
