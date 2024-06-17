from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from data.database.db import get_db
from schemas.notification import NotificationMessage
from schemas.notification import tokenCreate
from sqlalchemy.orm import Session
from services.notification import NotificationService



router = APIRouter()
@router.post('/send_notification', summary='Send a notification to a user.')
async def send_notification(message: NotificationMessage, db: Session = Depends(get_db)):
    service = NotificationService(db)
    token = service.send_notification_user(message)
    if token is None:
        return JSONResponse(status_code=404, content={"message": "Usuario no se encontro"})
    return JSONResponse(status_code=200, content={"token": token, "statusCode": 200})

@router.post("/save_token", summary="save token for notifications")
async def create_token(token: tokenCreate, db: Session = Depends(get_db)):
    try:
        service = NotificationService(db)
        token_create = service.post_token(token)
        return JSONResponse(
            status_code = status.HTTP_201_CREATED,
            content = {'data': token_create.model_dump()}
        )
    except Exception as e:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = {'data': None, 'message':'No se pudo guardar el token del dispositivo.', 'statusCode': status.HTTP_400_BAD_REQUEST}
        )