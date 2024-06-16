from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from data.database.db import get_db
from fastapi.encoders import jsonable_encoder
from services.user import UserService
from sqlalchemy.orm import Session
from schemas.user import UserRead


router = APIRouter()

@router.get("/users", response_model=list[UserRead], summary="Get all users.")
def get_all_users(db: Session = Depends(get_db)):
    service = UserService(db)
    users = service.all_users()
    if not users:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Not found users."})
    return JSONResponse(status_code=status.HTTP_200_OK, content={"data": jsonable_encoder(users)})