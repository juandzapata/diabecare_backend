from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from database.db import get_db
from schemas.notification import NotificationMessage
from schemas.notification import tokenCreate
from sqlalchemy.orm import Session
from services import notification



router = APIRouter()
@router.post('/send_notification', summary='Send a notification to a user.')
async def send_notification(message: NotificationMessage, db: Session = Depends(get_db)):
    token = notification.send_notification_user(message, db)
    if token is None:
        return JSONResponse(status_code=404, content={"message": "Usuario no se encontro"})
    return JSONResponse(status_code=200, content={"token": token, "statusCode": 200})

@router.post("/save_token", response_model=dict, summary="save token for notifications")
async def create_token(token: tokenCreate, db: Session = Depends(get_db)):
    token_creado = notification.post_token(token, db)
    if token_creado is None:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = f'Token is not added to the database, retry'
        )
    return JSONResponse(
        status_code = status.HTTP_201_CREATED,
        content = {'data': token_creado}
    )