from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from data.database.db import get_db
from fastapi.encoders import jsonable_encoder
from services.user import todos_los_usuarios
from sqlalchemy.orm import Session
from schemas.user import GetUser


router = APIRouter()

@router.get("/users", response_model=list[GetUser], summary="Get all users.")
def obtener_usuarios(db: Session = Depends(get_db)):
    usuarios = todos_los_usuarios(db)
    if not usuarios:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Not found users."})
    return JSONResponse(status_code=status.HTTP_200_OK, content={"data": jsonable_encoder(usuarios)})