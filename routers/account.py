from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from database.db import get_db
from middlewares.guards import NeedToken
from schemas.credentials_login import CredentialsLogin
from sqlalchemy.orm import Session
from services import account



router = APIRouter()
@router.post('/login',
             summary='Login a user in the database.')
def login(credentials: CredentialsLogin, db: Session = Depends(get_db)):
    token = account.login(credentials, db)
    if token is None:
        return JSONResponse(status_code=404, content={"message": "Usuario no se encontro"})
    return JSONResponse(status_code=200, content={"token": token})

@router.get('/validate_token',
            summary='Validate a token in the database.')
def validate_token(token: HTTPBearer = Depends(NeedToken()), db: Session = Depends(get_db)):
    token_data = account.validate_token(token=token, db=db)
    if token_data is None:
        return JSONResponse(status_code=404, content={"message": "token invalido"})
    return JSONResponse(status_code=200, content={"data": token_data})