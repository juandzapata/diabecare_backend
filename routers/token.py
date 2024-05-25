from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from schemas.token import tokenCreate
from database.db import get_db
from sqlalchemy.orm import Session

from services.token import post_token


router = APIRouter()

@router.post("/token", response_model=dict, summary="save token for notifications")
async def create_token(token: tokenCreate, db: Session = Depends(get_db)):
    token_creado = post_token(token, db)
    if token_creado is None:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = f'Token is not added to the database'
        )
    return JSONResponse(
        status_code = status.HTTP_201_CREATED,
        content = {'data': token_creado}
    )


