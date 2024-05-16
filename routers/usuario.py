from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from database.db import get_db
from fastapi.encoders import jsonable_encoder
from services.usuario import todos_los_usuarios
from sqlalchemy.orm import Session
from schemas.usuario import GetUsuario


router = APIRouter()

@router.get("/usuarios", response_model=list[GetUsuario], summary="Obtener todos los usuarios")
def obtener_usuarios(db: Session = Depends(get_db)):
    usuarios = todos_los_usuarios(db)
    if not usuarios:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "No hay usuarios registrados"})
    return JSONResponse(status_code=status.HTTP_200_OK, content={"data": jsonable_encoder(usuarios)})